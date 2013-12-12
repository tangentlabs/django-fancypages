from django.test import TestCase
from django.db.models import get_model

from fancypages.test import factories
from fancypages.templatetags import fp_sitemap_tags as sm_tags

FancyPage = get_model('fancypages', 'FancyPage')


class PageTreeMixin(object):

    def _create_grouped_pages(self):
        self.primary_nav_group = factories.PageGroupFactory(name="Primary Nav")
        self.footer_group = factories.PageGroupFactory(name="Footer")

        page_defaults = {'status': FancyPage.PUBLISHED}
        self.ungrouped_page = factories.FancyPageFactory(
            node__name='Ungrouped Page', **page_defaults)

        self.first_primnav_page = factories.FancyPageFactory(
            node__name="First primary navigation page", **page_defaults)
        self.first_primnav_page.groups.add(self.primary_nav_group)

        self.second_primnav_page = factories.FancyPageFactory(
            node__name="Second primary navigation page", **page_defaults)
        self.second_primnav_page.groups.add(self.primary_nav_group)

        self.footer_page = factories.FancyPageFactory(
            node__name="Footer page", **page_defaults)
        self.footer_page.groups.add(self.footer_group)

        self.both_groups_page = factories.FancyPageFactory(
            node__name="Both groups page", **page_defaults)
        self.both_groups_page.groups.add(self.primary_nav_group)
        self.both_groups_page.groups.add(self.footer_group)


class TestGetPagesTag(PageTreeMixin, TestCase):

    def setUp(self):
        super(TestGetPagesTag, self).setUp()
        self._create_grouped_pages()

    def test_returns_empty_queryset_for_unknown_page_group(self):
        with self.assertNumQueries(1):
            pages = sm_tags.get_pages(group='fantasy-group')
            self.assertSequenceEqual(pages, [])

    def test_returns_pages_for_group_slug_provided(self):
        with self.assertNumQueries(1):
            pages = sm_tags.get_pages(group=self.footer_group.slug)
            self.assertItemsEqual(
                pages,
                [self.footer_page, self.both_groups_page]
            )

    def test_returns_only_visible_pages(self):
        self.both_groups_page.status = FancyPage.DRAFT
        self.both_groups_page.save()

        with self.assertNumQueries(1):
            pages = sm_tags.get_pages(group=self.footer_group.slug)
            self.assertSequenceEqual(pages, [self.footer_page])

    def test_can_lookup_pages_from_group_object(self):
        with self.assertNumQueries(1):
            pages = sm_tags.get_pages(group=self.footer_group)
            self.assertItemsEqual(
                pages, [self.footer_page, self.both_groups_page])


class TestPageTreeTag(PageTreeMixin, TestCase):

    def setUp(self):
        super(TestPageTreeTag, self).setUp()
        self._create_grouped_pages()

        self.primnav_child = self.first_primnav_page.add_child(
            node__name="Primary Nav Child")
        self.footer_child = self.footer_page.add_child(
            node__name="Footer child")

    def test_returns_full_tree_with_depth_one(self):
        with self.assertNumQueries(1):
            page_tree = sm_tags.get_page_tree()

        self.assertEquals(page_tree, [
            (self.ungrouped_page, []),
            (self.first_primnav_page, []),
            (self.second_primnav_page, []),
            (self.footer_page, []),
            (self.both_groups_page, []),
        ])

    def test_returns_full_tree_with_depth_two(self):
        with self.assertNumQueries(1):
            page_tree = sm_tags.get_page_tree(depth=2)

        self.assertEquals(page_tree, [
            (self.ungrouped_page, []),
            (self.first_primnav_page, [
                (self.primnav_child, []),
            ]),
            (self.second_primnav_page, []),
            (self.footer_page, [
                (self.footer_child, []),
            ]),
            (self.both_groups_page, []),
        ])

    def test_returns_page_tree_without_primnav_child_with_depth_two(self):
        with self.assertNumQueries(1):
            page_tree = sm_tags.get_page_tree(
                group=self.primary_nav_group.slug, depth=2)

        self.assertEquals(page_tree, [
            (self.first_primnav_page, []),
            (self.second_primnav_page, []),
            (self.both_groups_page, []),
        ])

    def test_returns_primary_nav_tree_with_depth_two(self):
        self.primnav_child.groups.add(self.primary_nav_group)
        with self.assertNumQueries(1):
            page_tree = sm_tags.get_page_tree(
                group=self.primary_nav_group.slug, depth=2)

        self.assertEquals(page_tree, [
            (self.first_primnav_page, [
                (self.primnav_child, []),
            ]),
            (self.second_primnav_page, []),
            (self.both_groups_page, []),
        ])

    def test_returns_empty_page_tree_for_invalid_group(self):
        with self.assertNumQueries(1):
            page_tree = sm_tags.get_page_tree(group='invalid-group')

        self.assertSequenceEqual(page_tree, [])

    def test_returns_subpage_tree_relative_to_page(self):
        self.primnav_child.groups.add(self.primary_nav_group)
        with self.assertNumQueries(1):
            page_tree = sm_tags.get_page_tree(
                group=self.primary_nav_group,
                relative_to=self.first_primnav_page)
        self.assertSequenceEqual(page_tree, [(self.primnav_child, [])])
