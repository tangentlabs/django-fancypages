from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

import fancypages.urls
from fancypages import views

#from blog.views import PostDetailView, PostListView

admin.autodiscover()


urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name='home'),

    #url(r'^posts/$', PostListView.as_view(), name="post-list"),
    #url(r'^posts/(?P<slug>[\w-]+)/$', PostDetailView.as_view(),
    #    name="post-detail"),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),

    url(r'^', include(fancypages.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}))
