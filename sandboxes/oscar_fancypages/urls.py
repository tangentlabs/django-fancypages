from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

from oscar.app import Shop
from oscar.apps.catalogue.app import CatalogueApplication

import fancypages.urls
from fancypages.views import HomeView
from fancypages.contrib.oscar_fancypages import views


admin.autodiscover()


class FancyCatalogueApplication(CatalogueApplication):
    category_view = views.FancyPageDetailView


class FancyShop(Shop):
    catalogue_app = FancyCatalogueApplication()


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name="home"),

    url(r'', include(FancyShop().urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(fancypages.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}))
