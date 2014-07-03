# -*- coding: utf-8 -*-
import json

from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.utils.translation import get_language

from fancypages.test import factories
from fancypages.test import testcases
from fancypages.utils import get_node_model, get_page_model

PageType = get_model('fancypages', 'PageType')
PageNode = get_node_model()
FancyPage = get_page_model()
Container = get_model('fancypages', 'Container')
TextBlock = get_model('fancypages', 'TextBlock')
TabBlock = get_model('fancypages', 'TabBlock')
ContentBlock = get_model('fancypages', 'ContentBlock')


class TestTheBlockTypeApi(testcases.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestTheBlockTypeApi, self).setUp()
        self.container = Container.objects.create(name="test")

    def test_is_not_available_to_anonymous_users(self):
        self.app.get(reverse('fp-api:block-type-list'), status=403)

    def test_returns_a_block_type_form_for_container(self):
        page = self.get(
            reverse('fp-api:block-type-list'),
            params={'container': self.container.uuid})
        response = json.loads(page.content)
        self.assertIn('groupedBlocks', response)

    def test_returns_error_when_no_container_specified(self):
        response = self.get(reverse('fp-api:block-type-list'), status=400)
        self.assertIn('container ID is required', response.content)

    def test_returns_error_when_invalid_container_is_specified(self):
        response = self.get(reverse('fp-api:block-type-list'),
                            params={'container': 200}, status=400)
        self.assertIn('container ID is invalid', response.content)


class TestTheBlockApi(testcases.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestTheBlockApi, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}"
        )

        self.page = factories.FancyPageFactory(
            node__name="A new page", node__slug='a-new-page')

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

    def test_is_not_available_to_anonymous_users(self):
        response = self.app.get(reverse('fp-api:block-list'), status=403)
        self.assertIn('credentials were not provided', response.content)

    def test_can_be_added_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_blocks = container.blocks.count()
        response = self.post(
            reverse('fp-api:block-list'),
            params={'container': container.uuid, 'code': self.text_block.code})

        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.blocks.count(), num_blocks + 1)

        block_id = json.loads(response.content)['id']
        ContentBlock.objects.get_subclass(pk=block_id)

    def test_can_add_a_image_text_block_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_blocks = container.blocks.count()
        response = self.post(
            reverse('fp-api:block-list'),
            params={'container': container.uuid, 'code': 'image'})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.blocks.count(), num_blocks + 1)

        block_id = json.loads(response.content)['id']
        ContentBlock.objects.get_subclass(pk=block_id)


class TestTheBlockMoveApi(testcases.FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestTheBlockMoveApi, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container main-container %}"
            "{% fp_object_container left-container %}"
        )

        page_type = PageType.objects.create(
            name="Example Template",
            template_name=self.template_name,
        )
        self.page = factories.FancyPageFactory(
            node__name="A new page", node__slug='a-new-page',
            page_type=page_type)
        self.left_container = self.page.get_container_from_name(
            'left-container')
        self.main_container = self.page.get_container_from_name(
            'main-container')

        self.left_blocks = []
        self.main_blocks = []

        for idx in range(0, 3):
            main_block = TextBlock.objects.create(
                container=self.main_container,
                text="Main Column / Block #%d" % idx,
            )
            self.main_blocks.append(main_block)
            self.assertEquals(main_block.display_order, idx)

            left_block = TextBlock.objects.create(
                container=self.left_container,
                text="Left Column / Block #{}".format(idx))
            self.left_blocks.append(left_block)
            self.assertEquals(left_block.display_order, idx)

    def test_moves_a_block_up_within_a_container(self):
        for idx, pos in [(0, 0), (1, 1), (2, 2)]:
            block = TextBlock.objects.get(id=self.left_blocks[idx].id)
            self.assertEquals(block.display_order, pos)

        self.app.put(
            reverse('fp-api:block-move', kwargs={
                'uuid': self.main_blocks[1].uuid}),
            params={'container': self.left_container.uuid, 'index': 1},
            user=self.user)

        moved_block = TextBlock.objects.get(id=self.main_blocks[1].id)
        self.assertEquals(
            moved_block.container,
            self.page.get_container_from_name('left-container'))
        self.assertEquals(moved_block.display_order, 1)

        for idx, pos in [(0, 0), (1, 2), (2, 3)]:
            block = TextBlock.objects.get(id=self.left_blocks[idx].id)
            self.assertEquals(block.display_order, pos)

        for idx, pos in [(0, 0), (2, 1)]:
            block = TextBlock.objects.get(id=self.main_blocks[idx].id)
            self.assertEquals(block.display_order, pos)


class TestOrderedContainer(testcases.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def test_can_be_created_with_valid_uuid(self):
        self.block = factories.TabBlockFactory()

        params = {
            'block': self.block.uuid,
            'language_code': get_language()}

        self.post(reverse('fp-api:ordered-container-list'), params=params)
        self.assertEquals(TabBlock.objects.count(), 1)
        self.assertEquals(self.block.tabs.count(), 2)

    def test_cannot_be_created_with_invalid_uuid(self):
        params = {'block': 'invaliduuid', 'language_code': get_language()}

        response = self.post(reverse('fp-api:ordered-container-list'),
                             params=params, status=404)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(ContentBlock.objects.count(), 0)
