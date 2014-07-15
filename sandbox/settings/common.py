# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import django

import fancypages as fp

from configurations import Configuration, values


class Common(Configuration):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    SECRET_KEY = values.Value('insecure secret key')

    ADMINS = [('Sebastian Vetter', 'svetter@snowballdigital.com.au')]
    MANAGERS = ADMINS

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    TIME_ZONE = 'Australia/Melbourne'
    LANGUAGE_CODE = 'en-gb'
    LANGUAGES = (
        ('de', 'German'),
        ('en-gb', 'English'))

    ########## FANCYPAGES SETTINGS
    FP_FORM_BLOCK_CHOICES = {
        'contact-us': {
            'name': "Contact Us Form",
            'form': 'contact_us.forms.ContactUsForm',
            'url': 'contact-us',
            'template_name': 'contact_us/contact_us_form.html'}}
    ########## END FANCYPAGES SETTINGS

    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = []
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder')

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader')
    TEMPLATE_CONTEXT_PROCESSORS = [
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.request",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.contrib.messages.context_processors.messages"]
    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'fancypages.middleware.EditorMiddleware']

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',)

    LOGIN_URL = '/admin/login/'
    LOGIN_REDIRECT_URL = '/accounts/'
    APPEND_SLASH = True

    ALLOWED_HOSTS = ['*']
    SITE_ID = 1

    @property
    def ROOT_URLCONF(self):
        return "{}.urls".format(self.SANDBOX_MODULE)

    @property
    def WSGI_APPLICATION(self):
        return "{}.wsgi.application".format(self.SANDBOX_MODULE)

    @classmethod
    def pre_setup(cls):
        super(Common, cls).pre_setup()
        from fancypages.defaults import FANCYPAGES_SETTINGS
        for key, value in FANCYPAGES_SETTINGS.iteritems():
            if not hasattr(cls, key):
                setattr(cls, key, value)

    @property
    def TEMPLATE_DIRS(self):
        return [self.get_location('templates')]

    @property
    def MEDIA_ROOT(self):
        return self.get_location('public/media')

    @property
    def STATIC_ROOT(self):
        return self.get_location('public/static')

    @property
    def DATABASES(self):
        return {'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': self.get_location('db.sqlite3')}}

    @property
    def REQUIRED_APPS(self):
        apps = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin'] + fp.get_required_apps() + ['contact_us']

        if django.VERSION[1] < 7:
            apps.append('south')
        return apps

    @classmethod
    def get_location(cls, *path):
        """ Get absolute path for path relative to this file's directory. """
        path = (cls.SANDBOX_MODULE,) + path
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..', *path)
