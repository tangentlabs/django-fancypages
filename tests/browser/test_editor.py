# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import time
import pytest
import tempfile

from PIL import Image
from splinter.element_list import ElementList
from selenium.webdriver.common.keys import Keys

from django.db.models import get_model

from fancypages.test.fixtures import admin_user  # noqa
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


class TestTabBlock(SplinterTestCase):
    is_staff = True
    is_logged_in = True
    home_page_url = '/'

    def setUp(self):
        super(TestTabBlock, self).setUp()
        self.page = factories.FancyPageFactory()

    def test_tabs_can_be_added_and_removed(self):
        self.block = factories.TabBlockFactory(
            container=self.page.containers.all()[0])

        self.goto(self.page.get_absolute_url())
        self.find_and_click_by_css(self.browser, '#editor-handle')

        self.assertEqual(len(self.browser.find_by_css('.tab-pane')), 1)

        self.find_and_click_by_css(self.browser, '.fp-add-tab')
        self.wait_for_editor_reload()

        self.assertEqual(len(self.browser.find_by_css('.tab-pane')), 2)

        second_tab = self.browser.find_by_css('.fp-delete-tab')[0]
        second_tab_id = second_tab['data-block-id']
        second_tab.click()

        self.wait_for_editor_reload()

        self.assertEqual(len(self.browser.find_by_css('.tab-pane')), 1)
        tab_removed = self.browser.is_element_not_present_by_css(
            "[data-block-id='{}']".format(second_tab_id))
        if not tab_removed:
            self.fail("deleting the second tab failed")


def ensure_element(element_or_list, index=0):
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


def find_and_click_by_css(browser, selector, wait_time=3):
    browser.is_element_present_by_css(selector, wait_time)
    elem = ensure_element(browser.find_by_css(selector))
    return elem.click()


def open_editor_panel(browser):
    find_and_click_by_css(browser, '#editor-handle')
    if not browser.is_element_present_by_css('.edit-button', 2):
        raise AssertionError("Could not find edit button for block")


def wait_for_editor_reload(wait_for=3):
    time.sleep(wait_for)


@pytest.mark.browser
def test_text_block_can_be_added_to_a_container(admin_user, browser,
                                                live_server):
    fancypage = factories.FancyPageFactory()

    title = "Sample Title"
    text = "This is an amazing piece of text"
    factories.TitleTextBlockFactory(
        container=fancypage.containers.all()[0], title=title, text=text)

    browser.visit(live_server.url + fancypage.get_absolute_url())

    browser.is_text_present(title)
    browser.is_text_present(text)

    open_editor_panel(browser)

    find_and_click_by_css(browser, '.edit-button')
    wait_for_editor_reload()

    title_update = " Is Now New"
    browser.find_by_css('input[name=title]').type(title_update)
    browser.is_text_present(title + title_update)
    browser.is_text_present(text)

    text_update = " that I am editing on the fly."
    rte = browser.find_by_css('.trumbowyg-editor')
    rte.type(text_update)

    browser.is_text_present(text + text_update)
    browser.is_text_present(title + title_update)


@pytest.mark.browser
def test_text_block_can_be_deleted_from_a_container(admin_user, browser,
                                                    live_server):
    fancypage = factories.FancyPageFactory()
    title = "Sample Title"
    text = "This is an amazing piece of text"
    factories.TitleTextBlockFactory(
        container=fancypage.containers.all()[0], title=title, text=text)

    browser.visit(live_server.url + fancypage.get_absolute_url())

    browser.is_text_present(title)
    browser.is_text_present(text)

    open_editor_panel(browser)

    find_and_click_by_css(browser, 'div.delete')
    wait_for_editor_reload()

    assert factories.TitleTextBlockFactory._meta.model.objects.count() == 0


@pytest.mark.browser
def test_text_block_can_be_added_to_container(admin_user, browser,
                                              live_server):
    fancypage = factories.FancyPageFactory()

    browser.visit(live_server.url + fancypage.get_absolute_url())

    find_and_click_by_css(browser, '#editor-handle')
    find_and_click_by_css(browser, "div[class=block-add-control]>a")
    wait_for_editor_reload()

    find_and_click_by_css(browser, "a[href='#content']")

    find_and_click_by_css(browser, "button[data-block-code=text]")
    wait_for_editor_reload()

    default_text = 'Your text goes here'
    if not browser.is_text_present(default_text, 2):
        raise AssertionError("Could not find text block on page")

    if not browser.is_element_present_by_css('.edit-button', 2):
        raise AssertionError("Could not find edit button for block")

    find_and_click_by_css(browser, '.edit-button')
    wait_for_editor_reload()

    text_sel = 'textarea[name=text]'
    if not browser.is_element_present_by_css(text_sel, 2):
        raise AssertionError("Could not find input area for 'text' field")

    new_text = "The new text for this block"
    rte = browser.find_by_css('.trumbowyg-editor')
    # Jump to the end of the line and remove it using the backspace key
    rte.type(Keys.ARROW_RIGHT * (len(default_text) + 1))
    rte.type(Keys.BACKSPACE * (len(default_text) + 1))
    # Now add the new text
    rte.type(new_text)

    find_and_click_by_css(browser, 'button[type=submit]')
    wait_for_editor_reload()

    if not browser.is_text_present(new_text, 2):
        raise AssertionError("Could not find updated text")

    assert TextBlock.objects.count() == 1
    # check for the text with an appended <br> because typing text into
    # the input box via Selenium causes a linebreak at the end.
    assert TextBlock.objects.all()[0].text == new_text + '<br>'


@pytest.mark.browser
def test_can_be_added_with_new_image_and_link(admin_user, live_server,
                                              browser):
    fancypage = factories.FancyPageFactory()

    im = Image.new("RGB", (320, 240), "red")
    __, filename = tempfile.mkstemp(suffix='.jpg', dir=TEMP_MEDIA_ROOT)
    im.save(filename, "JPEG")

    image_filename = os.path.basename(filename)
    ImageAsset.objects.create(
        name='test image', image=image_filename, creator=admin_user)

    second_page = factories.FancyPageFactory(
        node__name='Another page', node__slug='another-page')

    browser.visit(live_server.url + fancypage.get_absolute_url())

    find_and_click_by_css(browser, '#editor-handle')
    find_and_click_by_css(browser, "div[class=block-add-control]>a")
    find_and_click_by_css(browser, "a[href='#content']")

    find_and_click_by_css(browser, "button[data-block-code=image]")
    wait_for_editor_reload()

    default_image_text = 'Add An Image'
    if not browser.is_text_present(default_image_text, 2):
        raise AssertionError("Could not find image block on page")

    if not browser.is_element_present_by_css('.edit-button', 2):
        raise AssertionError("Could not find edit button for block")

    find_and_click_by_css(browser, '.edit-button')
    wait_for_editor_reload()

    find_and_click_by_css(browser, 'a[data-behaviours=load-asset-modal]')
    wait_for_editor_reload()

    with browser.get_iframe(0) as iframe:
        wait_for_editor_reload()
        find_and_click_by_css(iframe, 'li[data-behaviours=selectable-asset]')

    wait_for_editor_reload()

    # select 'Another page' as the link for the image
    find_and_click_by_css(browser, '.glyphicon-share')
    find_and_click_by_css(browser, 'a[href*={}]'.format(second_page.slug))

    find_and_click_by_css(browser, 'button[type=submit]')
    wait_for_editor_reload()

    shows_image = browser.is_element_present_by_css(
        "img[src$='{}']".format(image_filename))
    if not shows_image:
        raise AssertionError('Image not added to image block')

    link_exists = browser.is_element_present_by_css(
        "div.block-wrapper>a[href*={}]".format(second_page.slug))

    if not link_exists:
        raise AssertionError(
            'image block is not wrapped in link to other page')
