from django.conf.urls.defaults import patterns, url, include

import fancypages.api.urls
from fancypages.api import API_BASE_URL
from fancypages.app import application as fancypages_app
from fancypages.dashboard.app import application as dashboard_app

urlpatterns = patterns('',
    url(r'dashboard/fancypages/', include(dashboard_app.urls)),
    url(
        API_BASE_URL,
        include(fancypages.api.urls, namespace='fp-api')
    ),
    url(r'', include(fancypages_app.urls)),
)
