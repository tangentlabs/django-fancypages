import os
import sys
import fancypages as fp

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fancypages.test import TEMP_MEDIA_ROOT

USE_OSCAR_SANDBOX = bool(os.getenv('USE_OSCAR_SANDBOX', False))

SANDBOX_MODULE = 'fancypages'
if USE_OSCAR_SANDBOX:
    SANDBOX_MODULE = 'oscar_fancypages'

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)
sandbox = lambda x: location("sandboxes/{}/{}".format(SANDBOX_MODULE, x))

sys.path.insert(0, sandbox('.'))


FP_OSCAR_SETTINGS = dict(
    FP_NODE_MODEL='catalogue.Category',
    FP_PAGE_DETAIL_VIEW='fancypages.contrib.oscar_fancypages.views.FancyPageDetailView',  # NOQA
    HAYSTACK_CONNECTIONS={
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }
)


def pytest_configure():
    from fancypages.defaults import FANCYPAGES_SETTINGS

    ADDITIONAL_SETTINGS = dict(
        LANGUAGE_CODE='en-gb',
        LANGUAGES=(
            ('de', _('German')),
            ('en-gb', _("English")),
        ),
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
        ] + fp.get_required_apps() + fp.get_fancypages_apps(
            use_with_oscar=USE_OSCAR_SANDBOX),
    )

    if USE_OSCAR_SANDBOX:
        from oscar.defaults import OSCAR_SETTINGS
        ADDITIONAL_SETTINGS.update(OSCAR_SETTINGS)

    ADDITIONAL_SETTINGS.update(FANCYPAGES_SETTINGS)

    if USE_OSCAR_SANDBOX:
        ADDITIONAL_SETTINGS.update(FP_OSCAR_SETTINGS)

        from oscar import get_core_apps
        ADDITIONAL_SETTINGS['INSTALLED_APPS'] += get_core_apps()

    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            MEDIA_ROOT=TEMP_MEDIA_ROOT,
            MEDIA_URL='/media/',
            STATIC_URL='/static/',
            STATICFILES_DIRS=[sandbox('static/')],
            STATIC_ROOT=sandbox('public'),
            STATICFILES_FINDERS=(
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            ),
            TEMPLATE_LOADERS=(
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
            TEMPLATE_CONTEXT_PROCESSORS = (
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.request",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.contrib.messages.context_processors.messages",
            ),
            MIDDLEWARE_CLASSES=(
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.locale.LocaleMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'fancypages.middleware.EditorMiddleware',
            ),
            ROOT_URLCONF='sandboxes.{}.sandbox.urls'.format(SANDBOX_MODULE),
            TEMPLATE_DIRS=[('templates')],
            AUTHENTICATION_BACKENDS=(
                'django.contrib.auth.backends.ModelBackend',
            ),
            LOGIN_REDIRECT_URL='/accounts/',
            APPEND_SLASH=True,
            SITE_ID=1,
            USE_OSCAR_SANDBOX=USE_OSCAR_SANDBOX,
            **ADDITIONAL_SETTINGS
        )
