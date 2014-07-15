# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os

from configurations import values
from django.utils.translation import ugettext_lazy as _

import fancypages as fp

from . import common


class OscarFancypages(common.Common):
    SANDBOX_MODULE = 'oscar_fancypages'

    @property
    def INSTALLED_APPS(self):
        from oscar import get_core_apps
        return self.REQUIRED_APPS + [
            'django.contrib.flatpages',
            'compressor',
        ] + fp.get_fancypages_apps(use_with_oscar=True) \
          + get_core_apps()

    MIDDLEWARE_CLASSES = common.Common.MIDDLEWARE_CLASSES + [
        'oscar.apps.basket.middleware.BasketMiddleware',
    ]

    AUTHENTICATION_BACKENDS = (
        'oscar.apps.customer.auth_backends.Emailbackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    ########## FANCYPAGES SETTINGS
    FP_NODE_MODEL = 'catalogue.Category'
    FP_PAGE_DETAIL_VIEW = 'fancypages.contrib.oscar_fancypages.views.FancyPageDetailView'  # noqa
    ########## END FANCYPAGES SETTINGS

    # Required for South < 1.0
    SOUTH_MIGRATION_MODULES = {
        'fancypages': 'fancypages.south_migrations',
        'oscar_fancypages': 'fancypages.contrib.oscar_fancypages.south_migrations',  # noqa
    }

    ########## OSCAR SETTINGS
    OSCAR_ALLOW_ANON_CHECKOUT = True

    TEMPLATE_CONTEXT_PROCESSORS = common.Common.TEMPLATE_CONTEXT_PROCESSORS + [
        'oscar.apps.search.context_processors.search_form',
        'oscar.apps.promotions.context_processors.promotions',
        'oscar.apps.checkout.context_processors.checkout',
        'oscar.apps.customer.notifications.context_processors.notifications',
        'oscar.core.context_processors.metadata',
    ]

    OSCAR_SHOP_NAME = 'FancyPages Sandbox'
    OSCAR_SHOP_TAGLINE = 'Make your pages sparkle and shine!'

    # Haystack settings
    HAYSTACK_CONNECTIONS = {
        'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'}}

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

    @property
    def TEMPLATE_DIRS(self):
        from oscar import OSCAR_MAIN_TEMPLATE_DIR
        return super(OscarFancypages, self).TEMPLATE_DIRS + [
            os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ]

    @classmethod
    def pre_setup(cls):
        """
        Set the default values for fancypages and oscar from their respective
        settings dictionaries before setting up/overwriting them on the
        configurations class.
        """
        super(OscarFancypages, cls).pre_setup()
        from oscar.defaults import OSCAR_SETTINGS
        for key, value in OSCAR_SETTINGS.iteritems():
            if not hasattr(cls, key):
                setattr(cls, key, value)


class OscarFancypagesPostgres(OscarFancypages):
    POSTGRES_PORT = values.Value(5432)

    @property
    def DATABASES(self):
        return {'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ofp_sandbox',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': self.POSTGRES_PORT}}


class OscarFancypagesMysql(OscarFancypages):
    MYSQL_PORT = values.Value(3306)

    @property
    def DATABASES(self):
        return {'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ofp_sandbox',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': self.MYSQL_PORT}}
