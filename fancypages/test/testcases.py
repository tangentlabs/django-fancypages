import os
import mock

from purl import URL

from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django import VERSION as DJANGO_VERSION
from django.core.management import call_command
from django.db import connections, DEFAULT_DB_ALIAS
from django.test import TestCase, LiveServerTestCase

from splinter import Browser

from fancypages.test import factories

SPLINTER_WEBDRIVER = getattr(
    settings,
    'SPLINTER_WEBDRIVER',
    os.environ.get('SPLINTER_WEBDRIVER', 'phantomjs')
)


class BlockTestCase(TestCase):

    def setUp(self):
        super(BlockTestCase, self).setUp()
        self.user = factories.UserFactory.build()

        self.request_context = RequestContext(mock.MagicMock())
        self.request_context['user'] = self.user

    def get_rendered_block(self, block):
        renderer = block.get_renderer_class()(block, self.request_context)
        return renderer.render()


class SplinterTestCase(LiveServerTestCase):
    username = 'peter.griffin'
    email = 'peter@griffin.com'
    password = 'lazyonthecouch'
    is_anonymous = True
    is_staff = False
    is_logged_in = True

    def setUp(self):
        settings.DEBUG = True
        super(SplinterTestCase, self).setUp()
        self.user = None
        self.base_url = URL(self.live_server_url)
        self.browser = Browser(SPLINTER_WEBDRIVER)

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
            self.assertIn('Log out', self.browser.html)

    def tearDown(self):
        super(SplinterTestCase, self).tearDown()
        self.browser.quit()

    def goto(self, path):
        url = self.base_url.path(path)
        return self.browser.visit(url.as_string())


# We need to patch the LiveServerTestCase here because the database in
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
