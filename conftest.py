import os
import sys

from django.conf import settings

import fancypages as fp
from fancypages.test import TEMP_MEDIA_ROOT

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x
)
sandbox = lambda x: location("sandbox/%s" % x)

sys.path.insert(0, location('sandbox'))



def pytest_configure():
    from fancypages.defaults import FANCYPAGES_SETTINGS

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
            STATICFILES_DIRS=[sandbox('static/') ],
            STATIC_ROOT=sandbox('public'),
            STATICFILES_FINDERS=(
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                'compressor.finders.CompressorFinder',
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
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'fancypages.middleware.EditorMiddleware',
            ),
            ROOT_URLCONF='sandbox.sandbox.urls',
            TEMPLATE_DIRS=[
                sandbox('templates'),
            ],
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',
                'blog',
            ] + fp.get_required_apps() + fp.get_fancypages_apps(),
            AUTHENTICATION_BACKENDS=(
                'django.contrib.auth.backends.ModelBackend',
            ),
            COMPRESS_ENABLED=True,
            COMPRESS_OFFLINE=False,
            COMPRESS_PRECOMPILERS=(
                ('text/less', 'lessc {infile} {outfile}'),
            ),
            LOGIN_REDIRECT_URL='/accounts/',
            APPEND_SLASH=True,
            SITE_ID=1,
            **FANCYPAGES_SETTINGS
        )
