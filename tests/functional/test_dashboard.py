# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import tempfile

from PIL import Image

from django.conf import settings
from django.utils import timezone
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date

from webtest import Upload

from fancypages.test import TEMP_IMAGE_DIR
from fancypages.test import testcases, factories
from fancypages.utils import get_page_model, get_node_model

PageType = get_model('fancypages', 'PageType')
FancyPage = get_page_model()


class TestAStaffMember(testcases.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.page_type = PageType.objects.create(name="Example Type")

    def test_can_create_a_new_toplevel_page(self):
        page = self.get(reverse('fp-dashboard:page-list'))
        page = page.click("Add New Page", index=0)

        self.assertContains(page, "Create new page")

        create_form = page.form
        create_form['name'] = "A new page"
        create_form['description'] = "Some description"
        create_form['page_type'] = self.page_type.id
        page = create_form.submit()

        self.assertRedirects(page, reverse('fp-dashboard:page-list'))
        page = page.follow()

        article_page = FancyPage.objects.get(node__name="A new page")

        self.assertEquals(article_page.status, FancyPage.DRAFT)
        self.assertEquals(article_page.is_visible, False)
        self.assertContains(page, u"not visible")

        self.assertEquals(article_page.description, "Some description")

    def test_update_a_toplevel_page(self):
        page_name = "Test page"
        page_description = "The old description"

        now = timezone.now()
        current_tz = timezone.get_current_timezone()

        fancy_page = factories.FancyPageFactory(
            date_visible_start=now, node__name=page_name,
            node__description=page_description)

        page = self.get(
            reverse('fp-dashboard:page-update', args=(fancy_page.id,)))

        self.assertContains(page, 'Update page')
        self.assertContains(page, fancy_page.name)

        form = page.form
        self.assertEquals(form['name'].value, page_name)
        self.assertEquals(form['description'].value.strip(), page_description)
        self.assertEquals(
            form['date_visible_start'].value,
            date(now.astimezone(current_tz), 'Y-m-d H:i:s'))

        form['name'] = 'Another name'
        form['description'] = "Some description"
        form['date_visible_start'] = '2012-12-30'
        page = form.submit()

        fancy_page = FancyPage.objects.get(id=fancy_page.id)
        self.assertEquals(fancy_page.name, 'Another name')
        self.assertEquals(fancy_page.description, 'Some description')

    def test_can_delete_a_page(self):
        fpage = factories.FancyPageFactory(node__name="A new page")
        self.assertEquals(FancyPage.objects.count(), 1)
        page = self.get(fpage.get_delete_page_url())
        page.forms['page-delete-form'].submit()
        self.assertEquals(FancyPage.objects.count(), 0)

    def test_can_cancel_the_delete_of_a_page(self):
        fpage = factories.FancyPageFactory(node__name="A new page")

        self.assertEquals(FancyPage.objects.count(), 1)

        page = self.get(fpage.get_delete_page_url())
        page = page.click('cancel')
        self.assertEquals(FancyPage.objects.count(), 1)
        self.assertContains(page, "Add New Page")
        self.assertContains(page, "Page Management")

    def test_can_delete_a_child_page(self):
        parent_page = factories.FancyPageFactory(node__name="A new page")
        factories.FancyPageFactory(node__name="Another page")

        child_page = parent_page.add_child(node__name="The child")

        parent = FancyPage.objects.get(id=parent_page.id)
        self.assertEquals(parent.node.numchild, 1)

        self.assertEquals(FancyPage.objects.count(), 3)
        page = self.get(child_page.get_delete_page_url())
        delete_page = page.forms['page-delete-form'].submit()
        self.assertRedirects(delete_page, reverse('fp-dashboard:page-list'))
        self.assertEquals(FancyPage.objects.count(), 2)

        p = FancyPage.objects.get(id=parent_page.id)
        self.assertSequenceEqual(p.node.get_children(), [])

        factories.FancyPageFactory(node__name="3rd page")
        self.assertEquals(FancyPage.objects.count(), 3)

    def test_can_create_child_page(self):
        child_page_name = 'Test Page'
        parent_page = factories.FancyPageFactory(node__name="A new page")

        create_form = self.get(parent_page.get_add_child_url()).form
        create_form['name'] = child_page_name
        list_page = create_form.submit()

        self.assertRedirects(list_page, reverse('fp-dashboard:page-list'))

        child_node = FancyPage.objects.get(node__name=child_page_name).node
        self.assertTrue(child_node.path.startswith(parent_page.node.path))
        self.assertTrue(child_node.depth, 2)


class TestANewPage(testcases.FancyPagesWebTest):
    is_staff = True

    def test_displays_an_error_when_slug_already_exists(self):
        page_title = "Home"
        home_page = factories.FancyPageFactory(node__name=page_title)
        self.assertEquals(home_page.slug, 'home')

        page = self.get(reverse('fp-dashboard:page-list'))

        page = page.click('Add New Page', index=0)
        new_page_form = page.form
        new_page_form['name'] = page_title
        page = new_page_form.submit()

        self.assertContains(page, 'A page with this title already exists')


class TestAnImageForAFancyPage(testcases.FancyPagesWebTest):
    is_staff = True

    def test_can_be_added_in_the_dashboard(self):
        fancy_page = factories.FancyPageFactory(node__name='Sample Page')
        self.assertEquals(fancy_page.image, None)

        im = Image.new("RGB", (320, 240), "red")
        __, filename = tempfile.mkstemp(suffix='.jpg', dir=TEMP_IMAGE_DIR)
        im.save(filename, "JPEG")

        page = self.get(
            reverse('fp-dashboard:page-update', args=(fancy_page.id,)))

        settings_form = page.form
        settings_form['image'] = Upload(filename)
        list_page = settings_form.submit()

        self.assertRedirects(list_page, reverse('fp-dashboard:page-list'))

        # This bit is required because when using Oscar, the upload directory
        # is defined by the category's image field and differs from the one on
        # the PageNode.
        upload_url = None
        for field in get_node_model()._meta.fields:
            if field.name == 'image':
                upload_url = field.upload_to
                break

        pages_path = os.path.join(settings.MEDIA_ROOT, upload_url)
        fancy_page = FancyPage.objects.get(id=fancy_page.id)
        self.assertEquals(
            fancy_page.image.path,
            os.path.join(pages_path, filename.rsplit('/')[-1]))
