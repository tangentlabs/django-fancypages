import os
#from PIL import Image
import tempfile

from django.core.files import File
from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages import test

User = get_model('auth', 'User')
Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
ImageAsset = get_model('assets', 'ImageAsset')
Container = get_model('fancypages', 'Container')
TextWidget = get_model('fancypages', 'TextWidget')
ImageWidget = get_model('fancypages', 'ImageWidget')
PageTemplate = get_model('fancypages', 'PageTemplate')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAWidget(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAWidget, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}"
        )

        self.page = Page.add_root(name="A new page", slug='a-new-page')

        self.text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text",
        )

        self.other_text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text",
        )

        self.third_text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="second text",
        )
        self.assertEquals(self.text_widget.display_order, 0)
        self.assertEquals(self.other_text_widget.display_order, 1)
        self.assertEquals(self.third_text_widget.display_order, 2)

    def test_can_be_deleted(self):
        page = self.get(reverse(
            'fp-dashboard:widget-delete',
            args=(self.third_text_widget.id,)
        ))
        # we need to fake a body as the template does not
        # contain that
        page.body = "<body>%s</body>" % page.body
        page = page.form.submit()

        self.assertEquals(TextWidget.objects.count(), 2)
        self.assertRaises(
            TextWidget.DoesNotExist,
            TextWidget.objects.get,
            id=self.third_text_widget.id
        )

    def test_can_be_deleted_and_remaining_widgets_are_reordered(self):
        page = self.get(reverse(
            'fp-dashboard:widget-delete',
            args=(self.other_text_widget.id,)
        ))
        # we need to fake a body as the template does not
        # contain that
        page.body = "<body>%s</body>" % page.body
        page = page.form.submit()

        self.assertEquals(TextWidget.objects.count(), 2)
        self.assertRaises(
            TextWidget.DoesNotExist,
            TextWidget.objects.get,
            id=self.other_text_widget.id
        )

        widget = TextWidget.objects.get(id=self.text_widget.id)
        self.assertEquals(widget.display_order, 0)

        widget = TextWidget.objects.get(id=self.third_text_widget.id)
        self.assertEquals(widget.display_order, 1)

    def test_a_widget_without_template_is_ignored(self):
        container = self.page.get_container_from_name('page-container')
        Widget.objects.create(container=container)
        self.get(reverse('fancypages:page-detail', args=(self.page.category.slug,)))


class TestAnAssetWidget(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAnAssetWidget, self).setUp()
        __, self.filename = tempfile.mkstemp(prefix="assetformtest", suffix='.jpg')
        im = Image.new("RGB", (200, 200), color=(255, 0, 0))
        im.save(self.filename, "JPEG")
        container = Container.objects.create(variable_name='test-container')
        self.image_asset = ImageAsset.objects.create(
            image=File(open(self.filename)),
            creator=self.user,
        )
        self.widget = ImageWidget.objects.create(container=container)

    def tearDown(self):
        os.remove(self.filename)

    def test_can_be_updated_when_no_asset_assigned(self):
        response = self.get(reverse('fp-dashboard:widget-update',
                                    args=(self.widget.id,)))
        response.form['image_asset_id'] = self.image_asset.pk
        response.form['image_asset_type'] = 'imageasset'
        page = response.form.submit().follow()

        widget = ImageWidget.objects.get(id=self.widget.id)
        self.assertEquals(widget.image_asset.id, self.image_asset.id)


class TestWidgetRendering(test.FancyPagesWebTest):

    def setUp(self):
        super(TestWidgetRendering, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}"
        )
        self.page = Page.add_root(name="A new page", slug='a-new-page')
        self.page.status = Page.PUBLISHED
        self.page.save()

    def test_for_all_widget_subclasses(self):
        for widget_class in Widget.get_widget_classes():
            container = self.page.containers.get(variable_name='page-container')
            widget = widget_class.objects.create(container=container)
            self.get(reverse(
                'fancypages:page-detail',
                args=(self.page.category.slug,)
            ))
            widget.delete()
