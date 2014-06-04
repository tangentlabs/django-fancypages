# -*- coding: utf-8 -*-
import os
import json
import time
import pytest
import requests

from functools import partial
from selenium.webdriver import ActionChains

from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages.test import factories

FancyPage = get_model('fancypages', 'FancyPage')

USE_REMOTE = os.getenv('TRAVIS', False) or os.getenv('USE_REMOTE', False)
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')


def report_test_result(request):
    passed = all([request.node.setup_report.failed,
                  request.node.call_report.failed])

    result = {'passed': passed}
    url = 'https://saucelabs.com/rest/v1/{username}/jobs/{job}'.format(
        username=SAUCE_USERNAME, job=request.session_id)

    print "Reporting to Sauce Labs:", url, result

    try:
        requests.put(url, data=json.dumps(result),
                     auth=(SAUCE_USERNAME, SAUCE_ACCESS_KEY))
    except requests.exceptions.RequestException as exc:
        print "Could not set test status in Sauce Labs:", unicode(exc)


@pytest.fixture
def splinter_webdriver():
    if USE_REMOTE:
        return 'remote'
    return 'firefox'


@pytest.fixture
def splinter_driver_kwargs(request):
    if not USE_REMOTE:
        return {}
    caps = {
        'browserName': 'firefox',
        'platform': "Linux",
        'version': "29"
    }
    if os.getenv('TRAVIS', False):
        caps['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
        caps['build'] = os.environ['TRAVIS_BUILD_NUMBER']
        caps['tags'] = [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']

    kwargs = {
        'url': "http://{}:{}@localhost:4445/wd/hub".format(
            SAUCE_USERNAME, SAUCE_ACCESS_KEY),
        'name': request.function.__name__,
        'desired_capabilities': caps}
    return kwargs


@pytest.fixture
def admin_user(request, live_server, browser):
    username = 'peter.griffin'
    email = 'peter@griffin.com'
    password = 'lazyonthecouch'

    user = factories.UserFactory(
        username=username, email=email, password=password, is_staff=True)

    browser.visit(live_server.url + reverse('admin:index'))
    browser.fill_form({'username': username, 'password': password})
    browser.find_by_css("input[type='submit']").first.click()

    if USE_REMOTE:
        request.session_id = browser.driver.session_id
        request.addfinalizer(partial(report_test_result, request))
    return user


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
