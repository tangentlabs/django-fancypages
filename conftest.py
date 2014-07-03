import os
import pytest
import django

from configurations import importer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Test')


def pytest_configure():
    importer.install()

    # Setup command is only available in Django 1.7+ but is required
    # to properly initialise the Django app config.
    if django.VERSION[1] >= 7:
        django.setup()


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    # execute all other hooks to obtain the report object
    rep = __multicall__.execute()
    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "{}_report".format(rep.when), rep)
    return rep


@pytest.fixture
def webtest_csrf_checks():
    return True


@pytest.fixture(scope='function')
def webtest(request, webtest_csrf_checks):
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
