import tempfile

from PIL import Image

from django.core.files import File
from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages import library
from fancypages.test import testcases
from fancypages.test import TEMP_IMAGE_DIR

User = get_model('auth', 'User')
FancyPage = get_model('fancypages', 'FancyPage')
ImageAsset = get_model('assets', 'ImageAsset')
Container = get_model('fancypages', 'Container')
TextBlock = get_model('fancypages', 'TextBlock')
ImageBlock = get_model('fancypages', 'ImageBlock')
ContentBlock = get_model('fancypages', 'ContentBlock')
TitleTextBlock = get_model('fancypages', 'TitleTextBlock')


class TestABlock(testcases.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestABlock, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}")

        self.page = FancyPage.add_root(
            node__name="A new page", node__slug='a-new-page')

        self.text_block = TextBlock.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text")

        self.other_text_block = TextBlock.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text")

        self.third_text_block = TextBlock.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="second text")
        self.assertEquals(self.text_block.display_order, 0)
        self.assertEquals(self.other_text_block.display_order, 1)
        self.assertEquals(self.third_text_block.display_order, 2)

    def test_can_be_deleted(self):
        self.delete(reverse('fp-api:block-detail',
                            kwargs={'uuid': self.third_text_block.uuid}))
        self.assertEquals(ContentBlock.objects.count(), 2)
        self.assertEquals(TextBlock.objects.count(), 2)
        with self.assertRaises(TextBlock.DoesNotExist):
            TextBlock.objects.get(id=self.third_text_block.id)

    def test_can_retrieve_block_form(self):
        response = self.get(
            reverse('fp-api:block-form', kwargs={
                'uuid': self.third_text_block.uuid}))

        data = response.json
        self.assertItemsEqual(
            data.keys(),
            [u'code', u'container', u'uuid', u'form', u'display_order'])

        self.assertIn('second text', data.get('form'))
        self.assertIn('name="text"', data.get('form'))
        self.assertIn(
            "data-block-id='{}'".format(self.third_text_block.uuid),
            data.get('form'))

    def test_can_be_deleted_and_remaining_blocks_are_reordered(self):
        self.assertEquals(TextBlock.objects.count(), 3)

        self.delete(reverse('fp-api:block-detail',
                            kwargs={'uuid': self.other_text_block.uuid}))

        self.assertEquals(TextBlock.objects.count(), 2)

        with self.assertRaises(TextBlock.DoesNotExist):
            TextBlock.objects.get(id=self.other_text_block.id)

        block = TextBlock.objects.get(id=self.text_block.id)
        self.assertEquals(block.display_order, 0)

        block = TextBlock.objects.get(id=self.third_text_block.id)
        self.assertEquals(block.display_order, 1)

    def test_a_block_without_template_is_ignored(self):
        container = self.page.get_container_from_name('page-container')
        ContentBlock.objects.create(container=container)
        self.get(self.page.get_absolute_url())


class TestAnAssetBlock(testcases.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestAnAssetBlock, self).setUp()

        im = Image.new("RGB", (200, 200), color=(255, 0, 0))
        __, self.filename = tempfile.mkstemp(suffix='.jpg', dir=TEMP_IMAGE_DIR)
        im.save(self.filename, "JPEG")
        container = Container.objects.create(name='test-container')
        self.image_asset = ImageAsset.objects.create(
            image=File(open(self.filename)),
            creator=self.user)
        self.block = ImageBlock.objects.create(container=container)

    def test_can_be_updated_with_asset_image(self):
        self.put(
            reverse('fp-api:block-detail', kwargs={'uuid': self.block.uuid}),
            params={'code': self.block.code,
                    'container': self.block.container.uuid,
                    'image_asset': self.image_asset.pk})

        block = ImageBlock.objects.get(id=self.block.id)
        self.assertEquals(block.image_asset.id, self.image_asset.id)


class TestBlockRendering(testcases.FancyPagesWebTest):

    def setUp(self):
        super(TestBlockRendering, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}")
        self.page = FancyPage.add_root(
            node__name="A new page", node__slug='a-new-page')
        self.page.status = FancyPage.PUBLISHED
        self.page.save()

    def test_for_all_block_subclasses(self):
        for block_class in library.get_content_blocks().values():
            container = self.page.containers.get(name='page-container')
            block = block_class.objects.create(container=container)
            self.get(self.page.get_absolute_url())
            block.delete()
