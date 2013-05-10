from django.conf.urls.defaults import patterns, url, include

from . import views

from fancypages.api import API_BASE_URL
from fancypages.api import app as api_app
from fancypages.dashboard import app as dashboard_app

urlpatterns = patterns('',
    url(r'^dashboard/fancypages/', include(dashboard_app.urls)),
    url(API_BASE_URL, include(api_app.urls)),
    url(
        r'^(?P<slug>[\w-]+(/[\w-]+)*)/$',
        views.FancyPageDetailView.as_view(),
        name='page-detail'
    ),
)
