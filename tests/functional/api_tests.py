from django.db.models import get_model
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from webtest import AppError

from fancypages import test

Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
Category = get_model('catalogue', 'Category')
PageType = get_model('fancypages', 'PageType')
Container = get_model('fancypages', 'Container')
TextWidget = get_model('fancypages', 'TextWidget')


class TestTheWidgetTypeApi(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestTheWidgetTypeApi, self).setUp()
        self.container = Container.objects.create(variable_name="test")

    def test_is_not_available_to_anonymous_users(self):
        try:
            self.app.get(reverse('fp-api:widget-type-list'))
            self.fail('an anonymous user should not be able to use the API')
        except AppError as exc:
            self.assertIn('You do not have permission', exc.message)
            self.assertIn('403', exc.args[0])

    def test_returns_a_widget_type_form_for_container(self):
        page = self.get(
            reverse('fp-api:widget-type-list'),
            params={
                'container': self.container.id,
            }
        )
        response = json.loads(page.content)
        self.assertIn('groupedWidgets', response)
        #self.assertIn('test_add_widget_form', response['rendered_form'])
        #self.assertIn('two-column-layout', response['rendered_form'])

    def test_returns_error_when_no_container_specified(self):
        try:
            self.get(reverse('fp-api:widget-type-list'))
            self.fail(
                'a container is required, this request should raise 400 error'
            )
        except AppError as exc:
            self.assertIn('container ID is required', exc.message)
            self.assertIn('400', exc.args[0])

    def test_returns_error_when_invalid_container_is_specified(self):
        try:
            self.get(
                reverse('fp-api:widget-type-list'),
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


class TestTheWidgetApi(test.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestTheWidgetApi, self).setUp()
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

    def test_is_not_available_to_anonymous_users(self):
        try:
            self.app.get(reverse('fp-api:widget-list'))
            self.fail('an anonymous user should not be able to use the API')
        except AppError as exc:
            self.assertIn('You do not have permission', exc.message)
            self.assertIn('403', exc.args[0])

    def test_can_be_added_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_widgets = container.widgets.count()
        response = self.post(
            reverse('fp-api:widget-list'),
            params={
                'container': container.id,
                'code': self.text_widget.code,
            },
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.widgets.count(), num_widgets + 1)

        widget_id = json.loads(response.content)['id']
        Widget.objects.get_subclass(pk=widget_id)

    def test_can_add_a_image_text_widget_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_widgets = container.widgets.count()
        response = self.post(
            reverse('fp-api:widget-list'),
            params={
                'container': container.id,
                'code': 'image',
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.widgets.count(), num_widgets + 1)

        widget_id = json.loads(response.content)['id']
        Widget.objects.get_subclass(pk=widget_id)


class TestTheWidgetMoveApi(test.FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestTheWidgetMoveApi, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container main-container %}"
            "{% fp_object_container left-container %}"
        )

        page_type = PageType.objects.create(
            name="Example Template",
            template_name=self.template_name,
        )
        self.page = Page.add_root(
            name="A new page",
            slug='a-new-page',
            page_type=page_type,
        )
        self.left_container = self.page.get_container_from_name('left-container')
        self.main_container = self.page.get_container_from_name('main-container')

        self.left_widgets = []
        self.main_widgets = []

        for idx in range(0, 3):
            main_widget = TextWidget.objects.create(
                container=self.main_container,
                text="Main Column / Widget #%d" % idx,
            )
            self.main_widgets.append(main_widget)
            self.assertEquals(main_widget.display_order, idx)

            left_widget = TextWidget.objects.create(
                container=self.left_container,
                text="Left Column / Widget #%d" % idx,
            )
            self.left_widgets.append(left_widget)
            self.assertEquals(left_widget.display_order, idx)

    def test_moves_a_widget_up_within_a_container(self):
        for idx, pos in [(0, 0), (1, 1), (2, 2)]:
            self.assertEquals(
                TextWidget.objects.get(id=self.left_widgets[idx].id).display_order,
                pos
            )

        self.app.put(
            reverse(
                'fp-api:widget-move',
                kwargs={
                    'pk': self.main_widgets[1].id,
                }
            ),
            params={
                'container': self.left_container.id,
                'index': 1,
            },
            user=self.user
        )

        moved_widget = TextWidget.objects.get(id=self.main_widgets[1].id)
        self.assertEquals(
            moved_widget.container,
            self.page.get_container_from_name('left-container')
        )
        self.assertEquals(moved_widget.display_order, 1)

        for idx, pos in [(0, 0), (1, 2), (2, 3)]:
            self.assertEquals(
                TextWidget.objects.get(id=self.left_widgets[idx].id).display_order,
                pos
            )

        for idx, pos in [(0, 0), (2, 1)]:
            self.assertEquals(
                TextWidget.objects.get(id=self.main_widgets[idx].id).display_order,
                pos
            )


class TestThePageMoveApi(test.FancyPagesWebTest):
    is_staff = True
    csrf_checks = False

    def setUp(self):
        super(TestThePageMoveApi, self).setUp()
        self.first_parent = Page.add_root(name="First parent")
        self.second_parent = Page.add_root(name="Second parent")
        self.third_parent = Page.add_root(name="Third parent")

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
            self.second_parent.category.id,
            Category.get_first_root_node().id
        )

    def test_can_move_root_page_into_parent_with_no_child(self):
        self.put(self.third_parent, {
            'parent': self.second_parent.id,
            'new_index': 0,
            'old_index': 1,
        })

        category = Category.objects.get(page=self.third_parent)
        self.assertEquals(category.path, '00020001')

    def test_can_move_child_page_to_first_root(self):
        self.put(self.a_child, {
            'parent': 0,
            'new_index': 0,
            'old_index': 1,
        })

        category = Category.objects.get(page=self.a_child)
        self.assertEquals(category.path, '0001')

    def test_can_move_child_page_to_last_root(self):
        self.put(self.a_child, {
            'parent': 0,
            'new_index': 2,
            'old_index': 1,
        })

        category = Category.objects.get(page=self.a_child)
        self.assertEquals(category.path, '0004')

    def test_can_move_root_page_into_parent_before_child(self):
        self.second_parent.add_child(name='Last child')

        self.put(self.third_parent, {
            'parent': self.second_parent.id,
            'new_index': 0,
            'old_index': 1,
        })

        category = Category.objects.get(page=self.third_parent)
        self.assertEquals(category.path, '00020001')

    def test_can_move_root_page_into_parent_after_child(self):
        child = self.second_parent.add_child(name='Last child')

        self.put(self.third_parent, {
            'parent': self.second_parent.id,
            'new_index': 1,
            'old_index': 1,
        })

        category = Category.objects.get(page=self.third_parent)
        self.assertEquals(category.path, '00020002')
        category = Category.objects.get(page=child)
        self.assertEquals(category.path, '00020001')

    def test_can_move_page_up_within_parent(self):
        first_child = self.second_parent.add_child(name='first child')
        second_child = self.second_parent.add_child(name='2nd child')

        self.put(second_child, {
            'parent': self.second_parent.id,
            'new_index': 0,
            'old_index': 1,
        })

        category = Category.objects.get(page=first_child)
        self.assertEquals(category.path, '00020002')
        category = Category.objects.get(page=second_child)
        self.assertEquals(category.path, '00020001')

    def test_can_move_page_down_within_parent(self):
        first_child = self.second_parent.add_child(name='first child')
        second_child = self.second_parent.add_child(name='2nd child')

        self.put(first_child, {
            'parent': self.second_parent.id,
            'new_index': 1,
            'old_index': 0,
        })

        category = Category.objects.get(page=first_child)
        self.assertEquals(category.path, '00020003')
        category = Category.objects.get(page=second_child)
        self.assertEquals(category.path, '00020002')
