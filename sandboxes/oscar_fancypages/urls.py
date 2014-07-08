# -*- coding: utf-8- -*-
from __future__ import absolute_import, unicode_literals
import django

from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

from oscar.app import Shop
from oscar.apps.catalogue.app import CatalogueApplication

import fancypages.urls
from fancypages.views import HomeView
from fancypages.contrib.oscar_fancypages import views
from contact_us.views import ContactUsView


# Auto-discovery for the admin is enabled by default in Djang 1.7
if django.VERSION[:3] < (1, 7):
    admin.autodiscover()


class FancyCatalogueApplication(CatalogueApplication):
    category_view = views.FancyPageDetailView


class FancyShop(Shop):
    catalogue_app = FancyCatalogueApplication()


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^contact-us/$', ContactUsView.as_view(), name='contact-us'),

    # i18n URLS need to live outside of i18n_patterns scope of the shop
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'', include(FancyShop().urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(fancypages.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}))
