from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages import test
from fancypages import library

User = get_model('auth', 'User')
FancyPage = get_model('fancypages', 'FancyPage')
ImageAsset = get_model('assets', 'ImageAsset')
Container = get_model('fancypages', 'Container')
TextBlock = get_model('fancypages', 'TextBlock')
ImageBlock = get_model('fancypages', 'ImageBlock')
PageTemplate = get_model('fancypages', 'PageTemplate')
ContentBlock = get_model('fancypages', 'ContentBlock')
TitleTextBlock = get_model('fancypages', 'TitleTextBlock')


class TestABlock(test.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestABlock, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}")

        self.page = FancyPage.add_root(name="A new page", slug='a-new-page')

        self.text_block = TextBlock.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text",
        )

        self.other_text_block = TextBlock.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text",
        )

        self.third_text_block = TextBlock.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="second text",
        )
        self.assertEquals(self.text_block.display_order, 0)
        self.assertEquals(self.other_text_block.display_order, 1)
        self.assertEquals(self.third_text_block.display_order, 2)

    def test_can_be_deleted(self):
        self.delete(reverse('fp-api:block-retrieve-update-destroy',
                            args=(self.third_text_block.id,)))
        self.assertEquals(ContentBlock.objects.count(), 2)
        self.assertEquals(TextBlock.objects.count(), 2)
        with self.assertRaises(TextBlock.DoesNotExist):
            TextBlock.objects.get(id=self.third_text_block.id)

    def test_can_retrieve_block_form(self):
        response = self.get(
            reverse('fp-api:block-form', kwargs={
                'pk': self.third_text_block.id}))
        raise NotImplementedError('needs validation of block form')


    #def test_can_be_deleted_and_remaining_blocks_are_reordered(self):
    #    page = self.get(reverse(
    #        'fp-dashboard:block-delete',
    #        args=(self.other_text_block.id,)
    #    ))
    #    # we need to fake a body as the template does not
    #    # contain that
    #    page.body = "<body>%s</body>" % page.body
    #    page = page.form.submit()

    #    self.assertEquals(TextBlock.objects.count(), 2)
    #    self.assertRaises(
    #        TextBlock.DoesNotExist,
    #        TextBlock.objects.get,
    #        id=self.other_text_block.id
    #    )

    #    block = TextBlock.objects.get(id=self.text_block.id)
    #    self.assertEquals(block.display_order, 0)

    #    block = TextBlock.objects.get(id=self.third_text_block.id)
    #    self.assertEquals(block.display_order, 1)

    def test_a_block_without_template_is_ignored(self):
        container = self.page.get_container_from_name('page-container')
        ContentBlock.objects.create(container=container)
        self.get(reverse('fancypages:page-detail', args=(self.page.slug,)))


#class TestAnAssetBlock(test.FancyPagesWebTest):
#    is_staff = True
#
#    def setUp(self):
#        super(TestAnAssetBlock, self).setUp()
#        __, self.filename = tempfile.mkstemp(prefix="assetformtest", suffix='.jpg')
#        im = Image.new("RGB", (200, 200), color=(255, 0, 0))
#        im.save(self.filename, "JPEG")
#        container = Container.objects.create(name='test-container')
#        self.image_asset = ImageAsset.objects.create(
#            image=File(open(self.filename)),
#            creator=self.user,
#        )
#        self.block = ImageBlock.objects.create(container=container)
#
#    def tearDown(self):
#        os.remove(self.filename)
#
#    def test_can_be_updated_when_no_asset_assigned(self):
#        response = self.get(reverse('fp-dashboard:block-update',
#                                    args=(self.block.id,)))
#        response.form['image_asset_id'] = self.image_asset.pk
#        response.form['image_asset_type'] = 'imageasset'
#        response.form.submit().follow()
#
#        block = ImageBlock.objects.get(id=self.block.id)
#        self.assertEquals(block.image_asset.id, self.image_asset.id)


class TestBlockRendering(test.FancyPagesWebTest):

    def setUp(self):
        super(TestBlockRendering, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}"
        )
        self.page = FancyPage.add_root(name="A new page", slug='a-new-page')
        self.page.status = FancyPage.PUBLISHED
        self.page.save()

    def test_for_all_block_subclasses(self):
        for block_class in library.get_content_blocks().values():
            container = self.page.containers.get(name='page-container')
            block = block_class.objects.create(container=container)
            self.get(reverse('fancypages:page-detail', args=(self.page.slug,)))
            block.delete()
