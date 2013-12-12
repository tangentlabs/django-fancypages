import time

from django.db.models import get_model

from fancypages.test import factories
from fancypages.test.testcases import SplinterTestCase

TextBlock = get_model('fancypages', 'TextBlock')


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


class TestATextBlock(SplinterTestCase):
    is_staff = True
    is_logged_in = True
    home_page_url = '/'

    def setUp(self):
        super(TestATextBlock, self).setUp()
        self.page = factories.PageFactory()

    def test_can_be_added_to_container(self):
        self.goto(self.page.get_absolute_url())
        self.browser.find_by_css('#editor-handle').click()

        self.browser.find_by_css("div[class=block-add-control]>a").click()
        self.browser.find_by_css("button[name=code][value=text]").click()

        default_text = 'Your text goes here'
        if not self.browser.is_text_present(default_text, 2):
            self.fail("Could not find text block on page")

        if not self.browser.is_element_present_by_css('.edit-button', 2):
            self.fail("Could not find edit button for block")

        self.browser.find_by_css('.edit-button').click()
        self.wait_for_editor_reload()

        text_sel = 'textarea[name=text]'
        if not self.browser.is_element_present_by_css(text_sel, 2):
            self.fail("Could not find input area for 'text' field")

        new_text = "The new text for this block"
        with self.browser.get_iframe(0) as iframe:
            ibody = iframe.find_by_css('body')
            ibody.type('\b' * (len(default_text) + 1))
            ibody.type(new_text)

        self.browser.find_by_css('button[type=submit]').click()
        self.wait_for_editor_reload()

        if not self.browser.is_text_present(new_text, 2):
            self.fail("Could not find updated text")

        self.assertEquals(TextBlock.objects.count(), 1)
        # check for the text with an appended <br> because typing text into
        # the input box via Selenium causes a linebreak at the end.
        self.assertEquals(TextBlock.objects.all()[0].text, new_text + '<br>')
