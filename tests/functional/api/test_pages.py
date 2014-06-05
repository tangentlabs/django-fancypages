# -*- coding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from fancypages.test import factories


@pytest.fixture
def webtest_csrf_checks():
    print "Disabling webtest CSRF check"
    return False


@pytest.fixture
def admin_user(db):
    user = factories.UserFactory(is_staff=True)
    return user


@pytest.mark.django_db
def test_get_list_of_pages(webtest, admin_user):
    top_level_1 = factories.FancyPageFactory()
    top_level_2 = factories.FancyPageFactory()
    top_level_3 = factories.FancyPageFactory()

    child_1 = factories.FancyPageFactory(node__parent=top_level_2)
    factories.FancyPageFactory(node__parent=child_1)
    factories.FancyPageFactory(node__parent=top_level_3)

    assert factories.FancyPageFactory.FACTORY_FOR.objects.count() == 6

    def get_page_as_json(page):
        children = []
        for child_page in page.get_children():
            children.append(get_page_as_json(child_page))

        parent_uuid = None
        if page.node.get_parent():
            parent_uuid = page.node.get_parent().page.uuid

        return {
            'uuid': page.uuid,
            'name': page.name,
            'parent': parent_uuid,
            'url': page.get_absolute_url(),
            'isVisible': page.is_visible,
            'status': page.status,
            'editPageUrl': page.get_edit_page_url(),
            'addChildUrl': page.get_add_child_url(),
            'deletePageUrl': page.get_delete_page_url(),
            'children': children}

    expected = [
        get_page_as_json(top_level_1),
        get_page_as_json(top_level_2),
        get_page_as_json(top_level_3)]

    response = webtest.get(reverse('fp-api:page-list'), user=admin_user)
    assert response.json == expected
