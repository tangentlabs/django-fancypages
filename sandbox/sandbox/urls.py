from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

import fancypages.urls
from fancypages import views

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(fancypages.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
