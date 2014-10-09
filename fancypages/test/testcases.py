# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import mock
import time
import pytest

from purl import URL

from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django import VERSION as DJANGO_VERSION
from django.core.management import call_command
from django.db import connections, DEFAULT_DB_ALIAS
from django.test import TestCase, LiveServerTestCase

from splinter import Browser
from splinter.element_list import ElementList

from django_webtest import WebTest

from fancypages.test import factories
from fancypages.compat import get_user_model
from fancypages.test.mixins import MockTemplateMixin

SPLINTER_WEBDRIVER = getattr(
    settings, 'SPLINTER_WEBDRIVER',
    os.environ.get('SPLINTER_WEBDRIVER', 'firefox'))

User = get_user_model()


class FancyPagesTestCase(TestCase, MockTemplateMixin):

    def setUp(self):
        super(FancyPagesTestCase, self).setUp()
        MockTemplateMixin.setUp(self)

    def tearDown(self):
        super(FancyPagesTestCase, self).tearDown()
        MockTemplateMixin.tearDown(self)


class FancyPagesWebTest(WebTest, MockTemplateMixin):
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'mysecretpassword'
    is_anonymous = True
    is_staff = False

    def setUp(self):
        super(FancyPagesWebTest, self).setUp()
        MockTemplateMixin.setUp(self)
        self.user = None

        if self.is_staff:
            self.is_anonymous = False

        if self.is_staff or not self.is_anonymous:
            self.user = User.objects.create_user(
                username=self.username, email=self.email,
                password=self.password)
            self.user.is_staff = self.is_staff
            self.user.save()

    def get(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.delete(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.put(*args, **kwargs)


class BlockTestCase(TestCase):

    def setUp(self):
        super(BlockTestCase, self).setUp()
        self.user = factories.UserFactory.build()

        self.request_context = RequestContext(mock.MagicMock())
        self.request_context['user'] = self.user

    def get_rendered_block(self, block):
        renderer = block.get_renderer_class()(block, self.request_context)
        return renderer.render()


@pytest.mark.browser
class SplinterTestCase(LiveServerTestCase):
    username = 'peter.griffin'
    email = 'peter@griffin.com'
    password = 'lazyonthecouch'
    is_anonymous = True
    is_staff = False
    is_logged_in = True

    def setUp(self):
        super(SplinterTestCase, self).setUp()
        self.user = None
        self.base_url = URL(self.live_server_url)
        self.browser = Browser(SPLINTER_WEBDRIVER)
        self.browser.driver.set_window_size(1280, 1024)

        if self.is_anonymous and not self.is_staff:
            return

        self.user = factories.UserFactory(
            username=self.username,
            email=self.email,
            password=self.password,
            is_staff=self.is_staff,
        )

        if self.is_logged_in:
            self.goto(reverse('admin:index'))
            self.browser.fill_form({
                'username': self.username,
                'password': self.password,
            })
            self.browser.find_by_css("input[type='submit']").first.click()
            exists = self.browser.is_text_present('Log out', wait_time=2)
            self.assertTrue(exists)

    def tearDown(self):
        super(SplinterTestCase, self).tearDown()
        if not os.getenv('SPLINTER_DEBUG'):
            self.browser.quit()

    def goto(self, path):
        url = self.base_url.path(path)
        return self.browser.visit(url.as_string())

    def wait_for_editor_reload(self, wait_for=3):
        time.sleep(wait_for)

    def ensure_element(self, element_or_list, index=0):
        """
        Selects either the element with *index* from the list of elements given
        in *element_or_list* or returns the single element if it is not a list.
        This make it possible to handle an element and a list of elements where
        only a single element is required.

        :param element: ``Element`` instance or ``ElementList``.
        :parem int index: Index of element to be returned if a list.
            (Default: 0)
        :rtype: Element
        """
        if isinstance(element_or_list, ElementList):
            return element_or_list[index]
        return element_or_list

    def find_and_click_by_css(self, browser, selector, wait_time=3):
        browser.is_element_present_by_css(selector, wait_time)
        elem = self.ensure_element(browser.find_by_css(selector))
        return elem.click()


# We need to patch the LiveServerTestCase here because the ORM in
# Django < 1.5.x doesn't clean up the database properly.
if DJANGO_VERSION[1] < 5:
    def _fixture_teardown(self):
        if getattr(self, 'multi_db', False):
            databases = connections
        else:
            databases = [DEFAULT_DB_ALIAS]
        for db in databases:
            call_command('flush', verbosity=0, interactive=False, database=db)

    SplinterTestCase._fixture_teardown = _fixture_teardown
