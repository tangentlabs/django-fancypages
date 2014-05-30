import os
import pytest
import tempfile

from django.db.models import get_model

from PIL import Image

from fancypages.test import TEMP_MEDIA_ROOT, factories
from fancypages.test.testcases import SplinterTestCase

TextBlock = get_model('fancypages', 'TextBlock')
ImageAsset = get_model('assets', 'ImageAsset')


class TestTheEditorPanel(SplinterTestCase):
    is_staff = True
    is_logged_in = True
    home_page_url = '/'

    def test_can_be_opened_by_clicking_the_handle(self):
        self.goto(self.home_page_url)
        body_tag = self.browser.find_by_css('body').first
        self.assertTrue(body_tag.has_class('editor-hidden'))

        self.find_and_click_by_css(self.browser, '#editor-handle')
        self.assertFalse(body_tag.has_class('editor-hidden'))

        try:
            value = self.browser.driver.get_cookie('fpEditorOpened')['value']
        except (KeyError, TypeError):
            self.fail("could not find cookie 'fpEditorOpened' but expected")

        self.assertEqual(value, 'true')

    def test_can_be_closed_by_clicking_the_x(self):
        self.assertEqual(
            self.browser.driver.get_cookie('fpEditorOpened'), None)

        self.goto(self.home_page_url)
        self.find_and_click_by_css(self.browser, '#editor-handle')
        body_tag = self.browser.find_by_css('body').first
        self.assertFalse(body_tag.has_class('editor-hidden'))

        self.find_and_click_by_css(self.browser, '#editor-close')
        body_tag = self.browser.find_by_css('body').first
        self.assertTrue(body_tag.has_class('editor-hidden'))

        try:
            value = self.browser.driver.get_cookie('fpEditorOpened')['value']
        except (KeyError, TypeError):
            self.fail("could not find cookie 'fpEditorOpened' but expected")

        self.assertEqual(value, u'false')

    def test_remains_opened_when_reloading_the_page(self):
        self.goto(self.home_page_url)
        self.find_and_click_by_css(self.browser, '#editor-handle')
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
        self.page = factories.FancyPageFactory()

    @pytest.mark.skipif(True,
                        reason=("there's an issue with splinter/selenium not "
                                "putting text into WYSIWYG editor textarea"))
    def test_can_be_added_to_container(self):
        self.goto(self.page.get_absolute_url())

        self.open_editor_panel()

        self.find_and_click_by_css(
            self.browser, "div[class=block-add-control]>a")

        self.find_and_click_by_css(self.browser, "a[href='#content']")

        self.find_and_click_by_css(
            self.browser, "button[data-block-code=text]")
        self.wait_for_editor_reload()

        default_text = 'Your text goes here'
        if not self.browser.is_text_present(default_text, 2):
            self.fail("Could not find text block on page")

        if not self.browser.is_element_present_by_css('.edit-button', 2):
            self.fail("Could not find edit button for block")

        self.find_and_click_by_css(self.browser, '.edit-button')
        self.wait_for_editor_reload()

        text_sel = 'textarea[name=text]'
        if not self.browser.is_element_present_by_css(text_sel, 2):
            self.fail("Could not find input area for 'text' field")

        new_text = "The new text for this block"
        with self.browser.get_iframe(0) as iframe:
            ibody = iframe.find_by_css('body')
            ibody.type('\b' * (len(default_text) + 1))
            ibody.type(new_text)

        self.find_and_click_by_css(self.browser, 'button[type=submit]')
        self.wait_for_editor_reload()

        if not self.browser.is_text_present(new_text, 2):
            self.fail("Could not find updated text")

        self.assertEquals(TextBlock.objects.count(), 1)
        # check for the text with an appended <br> because typing text into
        # the input box via Selenium causes a linebreak at the end.
        self.assertEquals(TextBlock.objects.all()[0].text, new_text + '<br>')

    def test_is_live_updated_when_editing(self):
        title = "Sample Title"
        text = "This is an amazing piece of text"
        factories.TitleTextBlockFactory(
            container=self.page.containers.all()[0], title=title, text=text)

        self.goto(self.page.get_absolute_url())

        self.browser.is_text_present(title)
        self.browser.is_text_present(text)

        self.open_editor_panel()

        self.find_and_click_by_css(self.browser, '.edit-button')
        self.wait_for_editor_reload()

        title_update = " Is Now New"
        self.browser.find_by_css('input[name=title]').type(title_update)
        self.browser.is_text_present(title + title_update)
        self.browser.is_text_present(text)

        text_update = " that I am editing on the fly."
        with self.browser.get_iframe(0) as iframe:
            ibody = iframe.find_by_css('body')
            ibody.type(text_update)
        self.browser.is_text_present(text + text_update)
        self.browser.is_text_present(title + title_update)

    def test_can_be_deleted_from_a_container(self):
        title = "Sample Title"
        text = "This is an amazing piece of text"
        factories.TitleTextBlockFactory(
            container=self.page.containers.all()[0], title=title, text=text)

        self.goto(self.page.get_absolute_url())

        self.browser.is_text_present(title)
        self.browser.is_text_present(text)

        self.open_editor_panel()

        self.find_and_click_by_css(self.browser, 'div.delete')
        self.wait_for_editor_reload()

        self.assertEqual(
            factories.TitleTextBlockFactory.FACTORY_FOR.objects.count(), 0)

    def open_editor_panel(self):
        self.find_and_click_by_css(self.browser, '#editor-handle')

        if not self.browser.is_element_present_by_css('.edit-button', 2):
            self.fail("Could not find edit button for block")


class TestImageBlock(SplinterTestCase):
    is_staff = True
    is_logged_in = True
    home_page_url = '/'

    def setUp(self):
        super(TestImageBlock, self).setUp()
        self.page = factories.FancyPageFactory()

        im = Image.new("RGB", (320, 240), "red")
        __, filename = tempfile.mkstemp(suffix='.jpg', dir=TEMP_MEDIA_ROOT)
        im.save(filename, "JPEG")

        self.image_filename = os.path.basename(filename)
        self.image = ImageAsset.objects.create(
            name='test image', image=self.image_filename, creator=self.user)

        self.page = factories.FancyPageFactory(
            node__name='Another page', node__slug='another-page')

    def test_can_be_added_with_new_image_and_link(self):
        self.goto(self.page.get_absolute_url())

        self.find_and_click_by_css(self.browser, '#editor-handle')

        self.find_and_click_by_css(
            self.browser, "div[class=block-add-control]>a")

        self.find_and_click_by_css(self.browser, "a[href='#content']")

        self.find_and_click_by_css(
            self.browser, "button[data-block-code=image]")
        self.wait_for_editor_reload()

        default_image_text = 'Add An Image'
        if not self.browser.is_text_present(default_image_text, 2):
            self.fail("Could not find image block on page")

        if not self.browser.is_element_present_by_css('.edit-button', 2):
            self.fail("Could not find edit button for block")

        self.find_and_click_by_css(self.browser, '.edit-button')
        self.wait_for_editor_reload()

        self.find_and_click_by_css(
            self.browser, 'a[data-behaviours=load-asset-modal]')
        self.wait_for_editor_reload()

        with self.browser.get_iframe(0) as iframe:
            self.wait_for_editor_reload()
            self.find_and_click_by_css(
                iframe, 'li[data-behaviours=selectable-asset]')

        self.wait_for_editor_reload()

        # select 'Another page' as the link for the image
        self.find_and_click_by_css(self.browser, '.glyphicon-share')
        self.find_and_click_by_css(
            self.browser, 'a[href="/{}/"]'.format(self.page.slug))

        self.find_and_click_by_css(self.browser, 'button[type=submit]')
        self.wait_for_editor_reload()

        shows_image = self.browser.is_element_present_by_css(
            "img[src$='{}']".format(self.image_filename))
        if not shows_image:
            self.fail('Image not added to image block')

        link_exists = self.browser.is_element_present_by_css(
            "div.block-wrapper>a[href='/{}/']".format(self.page.slug))

        if not link_exists:
            self.fail('image block is not wrapped in link to other page')
