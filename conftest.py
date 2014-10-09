# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import pytest
import django

from configurations import importer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'StandaloneTest')


def pytest_configure():
    importer.install()

    # Setup command is only available in Django 1.7+ but is required
    # to properly initialise the Django app config.
    if django.VERSION[1] >= 7:
        django.setup()


@pytest.fixture
def webtest_csrf_checks():
    return True


@pytest.fixture(scope='function')
def webtest(request, webtest_csrf_checks, transactional_db):
    """
    Provide the "app" object from WebTest as a fixture

    Taken and adapted from https://gist.github.com/magopian/6673250
    """
    from django_webtest import DjangoTestApp, WebTestMixin

    # Patch settings on startup
    wtm = WebTestMixin()
    wtm.csrf_checks = webtest_csrf_checks
    wtm._patch_settings()

    # Unpatch settings on teardown
    request.addfinalizer(wtm._unpatch_settings)

    return DjangoTestApp()


@pytest.fixture
def splinter_webdriver():
    return 'firefox'
