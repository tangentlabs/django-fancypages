from django.core.urlresolvers import reverse

from fancypages.test.testcases import SplinterTestCase


class TestTheEditorPanel(SplinterTestCase):
    is_staff = True
    is_logged_in = True
    home_page_url = '/'

    def _get_cookie_names(self):
        return [c.get('name') for c in self.browser.cookies.all()]

    def test_can_be_opened_by_clicking_the_handle(self):
        self.goto(self.home_page_url)
        body_tag = self.browser.find_by_css('body').first
        self.assertTrue(body_tag.has_class('editor-hidden'))

        self.browser.find_by_css('#editor-handle').click()
        self.assertFalse(body_tag.has_class('editor-hidden'))
        self.assertIn('fpEditorOpened', self._get_cookie_names())

    def test_can_be_closed_by_clicking_the_x(self):
        self.goto(self.home_page_url)
        self.browser.find_by_css('#editor-handle').click()
        body_tag = self.browser.find_by_css('body').first
        self.assertFalse(body_tag.has_class('editor-hidden'))

        self.browser.find_by_css('#editor-close').click()
        body_tag = self.browser.find_by_css('body').first
        self.assertTrue(body_tag.has_class('editor-hidden'))
        self.assertNotIn('fpEditorOpened', self._get_cookie_names())

    def test_remains_opened_when_reloading_the_page(self):
        self.goto(self.home_page_url)
        self.browser.find_by_css('#editor-handle').click()
        body_tag = self.browser.find_by_css('body').first
        self.assertFalse(body_tag.has_class('editor-hidden'))

        self.goto(self.home_page_url)
        body_tag = self.browser.find_by_css('body').first
        self.assertFalse(body_tag.has_class('editor-hidden'))
