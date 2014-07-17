# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest

from django.core.urlresolvers import reverse

from . import factories


@pytest.fixture
def admin_user(live_server, browser):
    username = 'peter.griffin'
    email = 'peter@griffin.com'
    password = 'lazyonthecouch'

    user = factories.UserFactory(
        username=username, email=email, password=password, is_staff=True)

    browser.visit(live_server.url + reverse('admin:index'))
    browser.fill_form({'username': username, 'password': password})
    browser.find_by_css("input[type='submit']").first.click()
    return user
