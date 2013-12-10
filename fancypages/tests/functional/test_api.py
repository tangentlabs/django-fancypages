from django.db.models import get_model
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from webtest import AppError

from fancypages import test

PageType = get_model('fancypages', 'PageType')
FancyPage = get_model('fancypages', 'FancyPage')
Container = get_model('fancypages', 'Container')
TextBlock = get_model('fancypages', 'TextBlock')
ContentBlock = get_model('fancypages', 'ContentBlock')


class TestTheBlockTypeApi(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestTheBlockTypeApi, self).setUp()
        self.container = Container.objects.create(name="test")

    def test_is_not_available_to_anonymous_users(self):
        try:
            self.app.get(reverse('fp-api:block-type-list'))
            self.fail('an anonymous user should not be able to use the API')
        except AppError as exc:
            self.assertIn('403', exc.args[0])

    def test_returns_a_block_type_form_for_container(self):
        page = self.get(
            reverse('fp-api:block-type-list'),
            params={
                'container': self.container.id,
            }
        )
        response = json.loads(page.content)
        self.assertIn('groupedBlocks', response)
        #self.assertIn('test_add_block_form', response['rendered_form'])
        #self.assertIn('two-column-layout', response['rendered_form'])

    def test_returns_error_when_no_container_specified(self):
        try:
            self.get(reverse('fp-api:block-type-list'))
            self.fail(
                'a container is required, this request should raise 400 error'
            )
        except AppError as exc:
            self.assertIn('container ID is required', exc.message)
            self.assertIn('400', exc.args[0])

    def test_returns_error_when_invalid_container_is_specified(self):
        try:
            self.get(
                reverse('fp-api:block-type-list'),
                params={
                    'container': 200,
                }
            )
            self.fail(
                'invalid container ID does not return 400 error'
            )
        except AppError as exc:
            self.assertIn('container ID is invalid', exc.message)
            self.assertIn('400', exc.args[0])


class TestTheBlockApi(test.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestTheBlockApi, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}"
        )

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

    def test_is_not_available_to_anonymous_users(self):
        try:
            self.app.get(reverse('fp-api:block-list'))
            self.fail('an anonymous user should not be able to use the API')
        except AppError as exc:
            #self.assertIn('You do not have permission', exc.message)
            self.assertIn('403', exc.args[0])

    def test_can_be_added_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_blocks = container.blocks.count()
        response = self.post(
            reverse('fp-api:block-list'),
            params={
                'container': container.id,
                'code': self.text_block.code,
            },
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.blocks.count(), num_blocks + 1)

        block_id = json.loads(response.content)['id']
        ContentBlock.objects.get_subclass(pk=block_id)

    def test_can_add_a_image_text_block_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_blocks = container.blocks.count()
        response = self.post(
            reverse('fp-api:block-list'),
            params={
                'container': container.id,
                'code': 'image',
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.blocks.count(), num_blocks + 1)

        block_id = json.loads(response.content)['id']
        ContentBlock.objects.get_subclass(pk=block_id)


class TestTheBlockMoveApi(test.FancyPagesWebTest):
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
        self.page = FancyPage.add_root(
            name="A new page",
            slug='a-new-page',
            page_type=page_type,
        )
        self.left_container = self.page.get_container_from_name('left-container')
        self.main_container = self.page.get_container_from_name('main-container')

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
                text="Left Column / Block #%d" % idx,
            )
            self.left_blocks.append(left_block)
            self.assertEquals(left_block.display_order, idx)

    def test_moves_a_block_up_within_a_container(self):
        for idx, pos in [(0, 0), (1, 1), (2, 2)]:
            self.assertEquals(
                TextBlock.objects.get(id=self.left_blocks[idx].id).display_order,
                pos
            )

        self.app.put(
            reverse('fp-api:block-move', kwargs={
                'uuid': self.main_blocks[1].uuid}),
            params={'container': self.left_container.id, 'index': 1},
            user=self.user)

        moved_block = TextBlock.objects.get(id=self.main_blocks[1].id)
        self.assertEquals(
            moved_block.container,
            self.page.get_container_from_name('left-container')
        )
        self.assertEquals(moved_block.display_order, 1)

        for idx, pos in [(0, 0), (1, 2), (2, 3)]:
            self.assertEquals(
                TextBlock.objects.get(id=self.left_blocks[idx].id).display_order,
                pos
            )

        for idx, pos in [(0, 0), (2, 1)]:
            self.assertEquals(
                TextBlock.objects.get(id=self.main_blocks[idx].id).display_order,
                pos
            )


class TestThePageMoveApi(test.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestThePageMoveApi, self).setUp()
        self.first_parent = FancyPage.add_root(name="First parent")
        self.second_parent = FancyPage.add_root(name="Second parent")
        self.third_parent = FancyPage.add_root(name="Third parent")

        self.a_child = self.first_parent.add_child(name='One child')
        self.first_parent.add_child(name='Another child')
        self.first_parent.add_child(name='Third child')

        #self.second_parent.add_child(name='Last child')

    def put(self, page, params):
        return self.app.put(
            reverse('fp-api:page-move', args=(page.id,)),
            params=params,
            user=self.user
        )

    def test_can_move_second_root_above_first(self):
        self.put(self.second_parent, {
            'parent': 0,
            'new_index': 0,
            'old_index': 1,
        })

        self.assertEquals(
            self.second_parent.id,
            FancyPage.get_first_root_node().id
        )

    def test_can_move_root_page_into_parent_with_no_child(self):
        self.put(self.third_parent, {
            'parent': self.second_parent.id,
            'new_index': 0,
            'old_index': 1,
        })
        page = FancyPage.objects.get(id=self.third_parent.id)
        self.assertEquals(page.path, '00020001')

    def test_can_move_child_page_to_first_root(self):
        self.put(self.a_child, {
            'parent': 0,
            'new_index': 0,
            'old_index': 1,
        })

        page = FancyPage.objects.get(id=self.a_child.id)
        self.assertEquals(page.path, '0001')

    def test_can_move_child_page_to_last_root(self):
        self.put(self.a_child, {
            'parent': 0,
            'new_index': 2,
            'old_index': 1,
        })

        page = FancyPage.objects.get(id=self.a_child.id)
        self.assertEquals(page.path, '0004')

    def test_can_move_root_page_into_parent_before_child(self):
        self.second_parent.add_child(name='Last child')

        self.put(self.third_parent, {
            'parent': self.second_parent.id,
            'new_index': 0,
            'old_index': 1,
        })

        page = FancyPage.objects.get(id=self.third_parent.id)
        self.assertEquals(page.path, '00020001')

    def test_can_move_root_page_into_parent_after_child(self):
        child = self.second_parent.add_child(name='Last child')

        self.put(self.third_parent, {
            'parent': self.second_parent.id,
            'new_index': 1,
            'old_index': 1,
        })

        page = FancyPage.objects.get(id=self.third_parent.id)
        self.assertEquals(page.path, '00020002')
        page = FancyPage.objects.get(id=child.id)
        self.assertEquals(page.path, '00020001')

    def test_can_move_page_up_within_parent(self):
        first_child = self.second_parent.add_child(name='first child')
        second_child = self.second_parent.add_child(name='2nd child')

        self.put(second_child, {
            'parent': self.second_parent.id,
            'new_index': 0,
            'old_index': 1,
        })

        page = FancyPage.objects.get(id=first_child.id)
        self.assertEquals(page.path, '00020002')
        page = FancyPage.objects.get(id=second_child.id)
        self.assertEquals(page.path, '00020001')

    def test_can_move_page_down_within_parent(self):
        first_child = self.second_parent.add_child(name='first child')
        second_child = self.second_parent.add_child(name='2nd child')

        self.put(first_child, {
            'parent': self.second_parent.id,
            'new_index': 1,
            'old_index': 0,
        })

        page = FancyPage.objects.get(id=first_child.id)
        self.assertEquals(page.path, '00020003')
        page = FancyPage.objects.get(id=second_child.id)
        self.assertEquals(page.path, '00020002')
