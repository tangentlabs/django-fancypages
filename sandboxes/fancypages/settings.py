# Django settings for sandbox project.
import os
import django

from configurations import Configuration, values


def get_location(*path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *path)


class FancypagesSandbox(Configuration):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    SOUTH_MIGRATION_MODULES = {
        'fancypages': 'fancypages.south_migrations',
        'fancypages.contrib.oscar_fancypages': 'fancypages.contrib.oscar_fancypages.south_migrations',  # noqa
    }

    ADMINS = [('Your Name', 'your_email@example.com')]
    MANAGERS = ADMINS

    SECRET_KEY = values.Value('insecure secret key')

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    TIME_ZONE = 'Australia/Melbourne'
    LANGUAGE_CODE = 'en-gb'
    LANGUAGES = (
        ('de', 'German'),
        ('en', 'English'),
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = get_location('public/media')

    STATIC_URL = '/static/'
    STATIC_ROOT = get_location('public/static')
    STATICFILES_DIRS = [get_location('static/')]
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )

    TEMPLATE_DIRS = [get_location('templates')]
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

    ROOT_URLCONF = 'urls'

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

    LOGIN_URL = '/admin/login/'

    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'wsgi.application'

    LOGIN_REDIRECT_URL = '/accounts/'
    APPEND_SLASH = True
    SITE_ID = 1
    ALLOWED_HOSTS = ['*']

    @classmethod
    def pre_setup(cls):
        super(FancypagesSandbox, cls).pre_setup()
        from fancypages.defaults import FANCYPAGES_SETTINGS
        for key, value in FANCYPAGES_SETTINGS.iteritems():
            setattr(cls, key, value)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': get_location('db.sqlite3')}}

    @property
    def INSTALLED_APPS(self):
        import fancypages as fp
        apps = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
        ] + fp.get_required_apps() + fp.get_fancypages_apps()

        if django.VERSION[1] < 7:
            apps.append('south')

        return apps


class FancypagesPostgres(FancypagesSandbox):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'fp_sandbox',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 5432}}


class FancypagesMysql(FancypagesSandbox):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fp_sandbox',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3306}}
