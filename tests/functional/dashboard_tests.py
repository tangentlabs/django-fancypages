from django.utils import timezone
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date

from fancypages import test

PageType = get_model('fancypages', 'PageType')
FancyPage = get_model('fancypages', 'FancyPage')


class TestAStaffMember(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.page_type = PageType.objects.create(name="Example Type")

    def test_can_create_a_new_toplevel_page(self):
        page = self.get(reverse('fp-dashboard:page-list'))
        page = page.click("Create new top-level page", index=0)

        self.assertContains(page, "Create new page")

        create_form = page.form
        create_form['name'] = "A new page"
        create_form['description'] = "Some description"
        create_form['page_type'] = self.page_type.id
        page = create_form.submit()

        self.assertRedirects(page, reverse('fp-dashboard:page-list'))
        page = page.follow()

        article_page = FancyPage.objects.get(name="A new page")
        # we use the default template for this page with only has one
        # container
        #self.assertEquals(article_page.containers.count(), 1)

        self.assertEquals(article_page.status, FancyPage.DRAFT)
        self.assertEquals(article_page.is_visible, False)
        self.assertContains(page, u"not visible")

        self.assertEquals(article_page.description, "Some description")

    def test_update_a_toplevel_page(self):
        page_name = "Test page"
        page_description = "The old description"

        now = timezone.now()

        fancy_page = FancyPage.add_root(name=page_name)
        fancy_page.date_visible_start = now
        fancy_page.description = page_description
        fancy_page.save()

        page = self.get(
            reverse('fp-dashboard:page-update', args=(fancy_page.id,))
        )
        self.assertContains(page, 'Update page')
        self.assertContains(page, fancy_page.name)

        form = page.form
        self.assertEquals(form['name'].value, page_name)
        self.assertEquals(form['description'].value, page_description)
        self.assertEquals(
            form['date_visible_start'].value,
            date(now, 'd-m-Y')
        )

        form['name'] = 'Another name'
        form['description'] = "Some description"
        form['date_visible_start'] = '30-12-2012'
        page = form.submit()

        fancy_page = FancyPage.objects.get(id=fancy_page.id)
        self.assertEquals(fancy_page.name, 'Another name')
        self.assertEquals(fancy_page.description, 'Some description')

    def test_can_delete_a_page(self):
        FancyPage.add_root(name="A new page")
        self.assertEquals(FancyPage.objects.count(), 1)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete")

        page.forms['page-delete-form'].submit()
        self.assertEquals(FancyPage.objects.count(), 0)

    def test_can_cancel_the_delete_of_a_page(self):
        FancyPage.add_root(name="A new page")

        self.assertEquals(FancyPage.objects.count(), 1)

        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete")
        page = page.click('cancel')
        self.assertEquals(FancyPage.objects.count(), 1)
        self.assertContains(page, "Create new top-level page")
        self.assertContains(page, "Page Management")

    def test_can_delete_a_child_page(self):
        parent_page = FancyPage.add_root(name="A new page")

        p = FancyPage.objects.get(id=parent_page.id)
        self.assertEquals(p.numchild, 0)

        FancyPage.add_root(name="Another page")
        parent_page.add_child(name="The child")

        p = FancyPage.objects.get(id=parent_page.id)
        self.assertEquals(p.numchild, 1)

        self.assertEquals(FancyPage.objects.count(), 3)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click(href="/dashboard/fancypages/delete/3/")

        page.forms['page-delete-form'].submit()
        self.assertEquals(FancyPage.objects.count(), 2)

        p = FancyPage.objects.get(id=parent_page.id)
        self.assertSequenceEqual(p.get_children(), [])

        FancyPage.add_root(name="3rd page")
        self.assertEquals(FancyPage.objects.count(), 3)


class TestANewPage(test.FancyPagesWebTest):
    is_staff = True

    def test_displays_an_error_when_slug_already_exists(self):
        page_title = "Home"
        home_page = FancyPage.add_root(name=page_title)
        self.assertEquals(home_page.slug, 'home')

        page = self.get(reverse('fp-dashboard:page-list'))
        self.assertContains(page, 'Home')

        page = page.click('Create new top-level page', index=0)
        new_page_form = page.form
        new_page_form['name'] = page_title
        page = new_page_form.submit()

        self.assertContains(page, 'A page with this title already exists')
