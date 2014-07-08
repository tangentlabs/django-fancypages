# -*- coding: utf-8- -*-
from __future__ import absolute_import, unicode_literals
import django

from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

from fancypages import views

from contact_us.views import ContactUsView


# Auto-discovery for the admin is enabled by default in Djang 1.7
if django.VERSION[:3] < (1, 7):
    admin.autodiscover()


urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact-us/$', ContactUsView.as_view(), name='contact-us'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),

    url(r'^', include('fancypages.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}))
