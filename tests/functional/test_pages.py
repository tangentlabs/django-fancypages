from webtest import AppError

from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages.test import FancyPagesWebTest


PageType = get_model('fancypages', 'PageType')
FancyPage = get_model('fancypages', 'FancyPage')
Container = get_model('fancypages', 'Container')
TitleTextBlock = get_model('fancypages', 'TitleTextBlock')


class TestAnAnonymousUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_anonymous = True

    def setUp(self):
        super(TestAnAnonymousUser, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container main-container %}"
            "{% fp_object_container left-column %}"
        )
        page_type = PageType.objects.create(
            name='template',
            template_name=self.template_name
        )
        self.page = FancyPage.add_root(
            name="A new page",
            slug='a-new-page',
            page_type=page_type,
        )

        self.left_container = self.page.get_container_from_name('left-column')
        self.main_container = self.page.get_container_from_name('main-container')

        self.main_block = TitleTextBlock.objects.create(
            container=self.main_container,
            title="This is the main title",
            text="The text of the main block",
        )

        self.left_block = TitleTextBlock.objects.create(
            container=self.left_container,
            title="This is the left title",
            text="The text of the left block",
        )

    def test_cannot_view_a_draft_page(self):
        self.assertRaises(
            AppError,
            self.get,
            reverse('fancypages:page-detail', args=(self.page.slug,))
        )

    def test_can_view_a_published_page(self):
        self.page.status = FancyPage.PUBLISHED
        self.page.save()

        page = self.get(reverse('fancypages:page-detail',
                                args=(self.page.slug,)))
        self.assertContains(page, self.left_block.title)
        self.assertContains(page, self.main_block.title)


class TestAStaffUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True

    def setUp(self):
        super(TestAStaffUser, self).setUp()
        self.page = FancyPage.add_root(name="A new page", slug='a-new-page')
        self.page_container = self.page.get_container_from_name('page-container')

        self.main_block = TitleTextBlock.objects.create(
            container=self.page_container,
            title="This is the main title",
            text="The text of the main block",
        )

    def test_can_view_a_draft_page(self):
        url = reverse('fancypages:page-detail', args=(self.page.slug,))
        page = self.get(url)

        self.assertContains(page, self.main_block.title)

        self.assertContains(
            page,
            ("You can only see this because you are logged in as "
             "a user with access rights to the dashboard")
        )

    def test_can_view_a_published_page(self):
        self.page.status = FancyPage.PUBLISHED
        self.page.save()

        page = self.get(reverse('fancypages:page-detail',
                                args=(self.page.slug,)))
        self.assertContains(page, self.main_block.title)

        self.assertNotContains(
            page,
            ("You can only see this because you are logged in as "
             "a user with access rights to the dashboard")
        )
