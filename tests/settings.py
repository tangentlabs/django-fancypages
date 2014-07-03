# -*- coding: utf-8 -*-
import os
import sys

from configurations import Configuration

from fancypages.test import TEMP_MEDIA_ROOT


class Test(Configuration):
    SANDBOX_MODULE = 'fancypages'
    SECRET_KEY = 'fake secret key'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    LANGUAGE_CODE = 'en-gb'
    LANGUAGES = (
        ('de', 'German'),
        ('en-gb', "English"),
    )

    MEDIA_ROOT = TEMP_MEDIA_ROOT
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.request",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.contrib.messages.context_processors.messages",
    )
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'fancypages.middleware.EditorMiddleware',
    )

    TEMPLATE_DIRS = [('templates')]

    LOGIN_REDIRECT_URL = '/accounts/'
    APPEND_SLASH = True
    SITE_ID = 1
    ALLOWED_HOSTS = ['*']

    @classmethod
    def pre_setup(cls):
        sys.path.insert(0, cls.get_sandbox('.'))
        super(Test, cls).pre_setup()
        from fancypages.defaults import FANCYPAGES_SETTINGS
        for key, value in FANCYPAGES_SETTINGS.iteritems():
            setattr(cls, key, value)

    @property
    def ROOT_URLCONF(cls):
        return 'sandboxes.{}.urls'.format(cls.SANDBOX_MODULE)

    @property
    def INSTALLED_APPS(self):
        import fancypages as fp
        return [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
        ] + fp.get_required_apps() + fp.get_fancypages_apps()

    @property
    def STATICFILES_DIRS(self):
        return [self.get_sandbox('static/')]

    @property
    def STATIC_ROOT(self):
        return self.get_sandbox('public')

    @classmethod
    def get_location(cls, *path):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), *path)

    @classmethod
    def get_sandbox(cls, *path):
        return cls.get_location(
            "sandboxes/{}/{}".format(cls.SANDBOX_MODULE, *path))


class OscarTest(Test):
    SANDBOX_MODULE = 'oscar_fancypages'

    FP_NODE_MODEL = 'catalogue.Category',
    FP_PAGE_DETAIL_VIEW = 'fancypages.contrib.oscar_fancypages.views.FancyPageDetailView',  # noqa
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

    @property
    def INSTALLED_APPS(self):
        import fancypages as fp
        from oscar import get_core_apps
        return [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django.contrib.flatpages',
        ] + fp.get_required_apps() + \
            fp.get_fancypages_apps(use_with_oscar=True) + \
            get_core_apps()

    @classmethod
    def pre_setup(cls):
        super(Test, cls).pre_setup()
        from oscar.defaults import OSCAR_SETTINGS
        for key, value in OSCAR_SETTINGS.iteritems():
            setattr(cls, key, value)

        from fancypages.defaults import FANCYPAGES_SETTINGS
        for key, value in FANCYPAGES_SETTINGS.iteritems():
            setattr(cls, key, value)
