import os
import sys
import mock
import time
import json
import pytest
import requests

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

SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

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

    use_remote = os.getenv('TRAVIS', False) or os.getenv('USE_REMOTE', False)

    def get_remote_browser(self):
        remote_url = "http://{}:{}@localhost:4445/wd/hub".format(
            SAUCE_USERNAME, SAUCE_ACCESS_KEY)

        caps = {
            'name': getattr(self, 'name', self.__class__.__name__),
            'browser': 'firefox',
            'platform': "Linux",
            'version': "29"}

        if os.getenv('TRAVIS', False):
            caps['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            caps['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            caps['tags'] = [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']

        return Browser(driver_name='remote', url=remote_url, **caps)

    def get_local_browser(self):
        return Browser(SPLINTER_WEBDRIVER)

    def setUp(self):
        super(SplinterTestCase, self).setUp()
        self.user = None
        self.base_url = URL(self.live_server_url)

        if self.use_remote:
            self.browser = self.get_remote_browser()
        else:
            self.browser = self.get_local_browser()

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

    def report_test_result(self):
        result = {'passed': sys.exc_info() == (None, None, None)}
        url = 'https://saucelabs.com/rest/v1/{username}/jobs/{job}'.format(
            username=SAUCE_USERNAME, job=self.browser.driver.session_id)

        try:
            response = requests.put(url, data=json.dumps(result),
                                    auth=(SAUCE_USERNAME, SAUCE_ACCESS_KEY))
        except requests.exceptions.RequestsExceptions:
            print "Could not set test status in Sauce Labs."
        return response.status_code == requests.codes.ok

    def tearDown(self):
        super(SplinterTestCase, self).tearDown()
        if not os.getenv('SPLINTER_DEBUG'):
            self.browser.quit()

        if self.use_remote:
            self.report_test_result()

    def goto(self, path):
        url = self.base_url.path(path)
        return self.browser.visit(url.as_string())

    def wait_for_editor_reload(self, wait_for=3):
        if self.use_remote:
            wait_for += 5
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
