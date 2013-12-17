from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

from oscar.app import Shop
from oscar.apps.catalogue.app import CatalogueApplication

#from oscar_fancypages.fancypages.views import FancyHomeView
from fancypages.views import HomeView
from fancypages.contrib.oscar_fancypages import views

from fancypages.api import API_BASE_URL
from fancypages.app import application as fancypages_app
from fancypages.dashboard.app import application as dashboard_app


admin.autodiscover()


class FancyCatalogueApplication(CatalogueApplication):
    category_view = views.FancyPageDetailView


class FancyShop(Shop):
    catalogue_app = FancyCatalogueApplication()


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name="home"),

    url(r'', include(FancyShop().urls)),

    url(r'^dashboard/fancypages/', include(dashboard_app.urls)),
    url(API_BASE_URL, include('fancypages.api.urls', namespace='fp-api')),
    url(r'^', include(fancypages_app.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
