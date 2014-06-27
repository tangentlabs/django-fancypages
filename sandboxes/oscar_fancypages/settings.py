# Django settings for sandbox project.
import os
import django
import fancypages as fp

from django.utils.translation import ugettext_lazy as _

from configurations import Configuration, values

from oscar import OSCAR_MAIN_TEMPLATE_DIR


def get_location(*path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *path)


class OscarFancypagesSandbox(Configuration):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    USE_LESS = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': get_location('db.sqlite3')}}

    SOUTH_MIGRATION_MODULES = {
        'fancypages': 'fancypages.south_migrations',
        'oscar_fancypages': 'fancypages.contrib.oscar_fancypages.south_migrations',  # noqa
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

    STATICFILES_DIRS = [
    ] + fp.get_fancypages_paths('static', use_with_oscar=True)

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )

    TEMPLATE_DIRS = [get_location('templates')]

    TEMPLATE_DIRS = [
        get_location('templates'),
    ] + fp.get_fancypages_paths('templates', use_with_oscar=True) + [
        os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
        OSCAR_MAIN_TEMPLATE_DIR,
    ]

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
        # Oscar specific
        'oscar.apps.search.context_processors.search_form',
        'oscar.apps.promotions.context_processors.promotions',
        'oscar.apps.checkout.context_processors.checkout',
        'oscar.apps.customer.notifications.context_processors.notifications',
        'oscar.core.context_processors.metadata',
    )
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'oscar.apps.basket.middleware.BasketMiddleware',
        'fancypages.middleware.EditorMiddleware',
    )

    ROOT_URLCONF = 'urls'

    AUTHENTICATION_BACKENDS = (
        'oscar.apps.customer.auth_backends.Emailbackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    LOGIN_URL = '/admin/login/'

    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'wsgi.application'

    LOGIN_REDIRECT_URL = '/accounts/'
    APPEND_SLASH = True
    SITE_ID = 1
    ALLOWED_HOSTS = ['*']

    ########## FANCYPAGES SETTINGS
    FP_NODE_MODEL = 'catalogue.Category'
    FP_PAGE_DETAIL_VIEW = 'fancypages.contrib.oscar_fancypages.views.FancyPageDetailView'  # noqa
    ########## END FANCYPAGES SETTINGS

    ########## OSCAR SETTINGS
    OSCAR_ALLOW_ANON_CHECKOUT = True

    OSCAR_SHOP_NAME = 'FancyPages Sandbox'
    OSCAR_SHOP_TAGLINE = 'Make your pages sparkle and shine!'

    # Haystack settings
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }
    OSCAR_DASHBOARD_NAVIGATION = [
        {
            'label': _('Dashboard'),
            'icon': 'icon-th-list',
            'url_name': 'dashboard:index',
        },
        {
            'label': _('Catalogue'),
            'icon': 'icon-sitemap',
            'children': [
                {
                    'label': _('Products'),
                    'url_name': 'dashboard:catalogue-product-list',
                },
                {
                    'label': _('Pages / Categories'),
                    'url_name': 'fp-dashboard:page-list',
                },
                {
                    'label': _('Ranges'),
                    'url_name': 'dashboard:range-list',
                },
                {
                    'label': _('Low stock alerts'),
                    'url_name': 'dashboard:stock-alert-list',
                },
            ]
        },
        {
            'label': _('Fulfilment'),
            'icon': 'icon-shopping-cart',
            'children': [
                {
                    'label': _('Order management'),
                    'url_name': 'dashboard:order-list',
                },
                {
                    'label': _('Statistics'),
                    'url_name': 'dashboard:order-stats',
                },
            ]
        },
        {
            'label': _('Customers'),
            'icon': 'icon-group',
            'children': [
                {
                    'label': _('Customer management'),
                    'url_name': 'dashboard:users-index',
                },
                {
                    'label': _('Stock alert requests'),
                    'url_name': 'dashboard:user-alert-list',
                },
            ]
        },
        {
            'label': _('Offers'),
            'icon': 'icon-bullhorn',
            'children': [
                {
                    'label': _('Offer management'),
                    'url_name': 'dashboard:offer-list',
                },
                {
                    'label': _('Vouchers'),
                    'url_name': 'dashboard:voucher-list',
                },
            ],
        },
        {
            'label': _('Content'),
            'icon': 'icon-folder-close',
            'children': [
                {
                    'label': _('Content blocks'),
                    'url_name': 'dashboard:promotion-list',
                },
                {
                    'label': _('Content blocks by page'),
                    'url_name': 'dashboard:promotion-list-by-page',
                },
                {
                    'label': _('Pages'),
                    'url_name': 'dashboard:page-list',
                },
                {
                    'label': _('Email templates'),
                    'url_name': 'dashboard:comms-list',
                },
                {
                    'label': _('Reviews'),
                    'url_name': 'dashboard:reviews-list',
                },
            ]
        },
        {
            'label': _('Reports'),
            'icon': 'icon-bar-chart',
            'url_name': 'dashboard:reports-index',
        },
    ]
    ########## END OSCAR SETTINGS

    @classmethod
    def pre_setup(cls):
        """
        Set the default values for fancypages and oscar from their respective
        settings dictionaries before setting up/overwriting them on the
        configurations class.
        """
        super(OscarFancypagesSandbox, cls).pre_setup()
        from fancypages.defaults import FANCYPAGES_SETTINGS
        for key, value in FANCYPAGES_SETTINGS.iteritems():
            setattr(cls, key, value)
        from oscar.defaults import OSCAR_SETTINGS
        for key, value in OSCAR_SETTINGS.iteritems():
            setattr(cls, key, value)

    def INSTALLED_APPS(self):
        from oscar import get_core_apps

        apps = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'compressor',
        ] + fp.get_required_apps() \
          + fp.get_fancypages_apps(use_with_oscar=True) \
          + get_core_apps()

        if django.VERSION[1] < 7:
            apps.append('south')

        return apps


class OscarFancypagesPostgres(OscarFancypagesSandbox):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ofp_sandbox',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 5432}}


class OscarFancypagesMysql(OscarFancypagesSandbox):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ofp_sandbox',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': 3306}}
