# -*- coding: utf-8 -*-
import time
import pytest

from selenium.webdriver import ActionChains

from django.db.models import get_model

from fancypages.test import factories
from fancypages.test.fixtures import admin_user  # noqa

FancyPage = get_model('fancypages', 'FancyPage')


@pytest.mark.browser
def test_can_move_block_from_one_container_to_another(live_server, browser,
                                                      admin_user):
    page = factories.FancyPageFactory(node__name='Home')
    main_container = page.containers.all()[0]

    layout = factories.TwoColumnLayoutBlockFactory(container=main_container)
    browser.visit(live_server.url + page.get_absolute_url())

    right = layout.containers.get(name='right-container')
    left = layout.containers.get(name='left-container')

    moving_block = factories.TextBlockFactory(container=right)
    factories.TextBlockFactory(container=right)
    factories.TextBlockFactory(container=left)

    browser.visit(live_server.url + page.get_absolute_url())
    browser.find_by_css('#editor-handle').first.click()

    source = browser.find_by_css(
        '#block-{} div.move'.format(moving_block.uuid)).first

    chain = ActionChains(browser.driver)
    chain.drag_and_drop_by_offset(source._element, -600, 200).perform()

    time.sleep(5)

    assert right.blocks.count() == left.blocks.count() == 1
    assert main_container.blocks.count() == 2

    main_block_ids = [b.uuid for b in main_container.blocks.all()]
    assert main_block_ids == [layout.uuid, moving_block.uuid]
