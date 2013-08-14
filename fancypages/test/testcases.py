from purl import URL

from django.conf import settings
from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from splinter import Browser

from fancypages.test import factories

SPLINTER_WEBDRIVER = getattr(settings, 'SPLINTER_WEBDRIVER', 'phantomjs')


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
