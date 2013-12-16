from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

from oscar.app import shop

#from oscar_fancypages.fancypages.views import FancyHomeView

from fancypages.api import API_BASE_URL
from fancypages.app import application as fancypages_app
from fancypages.dashboard.app import application as dashboard_app
from fancypages.contrib.oscar_fancypages.app import application as ofp_app


admin.autodiscover()


urlpatterns = patterns(
    '',
    #url(r'^$', FancyHomeView.as_view(), name="home"),

    url(r'', include(shop.urls)),

    url(r'^dashboard/fancypages/', include(dashboard_app.urls)),
    url(API_BASE_URL, include('fancypages.api.urls', namespace='fp-api')),

    url(r'^', include(ofp_app.urls)),
    url(r'^', include(fancypages_app.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
