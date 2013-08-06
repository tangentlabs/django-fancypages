from django.conf.urls import patterns, url

from fancypages.api import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ApiV2View.as_view(), name="api-root"),
    url(r'^blocks$', views.BlockListView.as_view(), name='block-list'),
    url(
        r'^block/(?P<pk>\d+)$',
        views.BlockRetrieveUpdateDestroyView.as_view(),
        name='block-retrieve-update-destroy'
    ),
    url(
        r'^block/(?P<pk>\d+)/move$',
        views.BlockMoveView.as_view(),
        name='block-move'
    ),
    url(
        r'^ordered-containers$',
        views.OrderedContainerListView.as_view(),
        name='ordered-container-list'
    ),
    url(
        r'^block-types$',
        views.BlockTypesView.as_view(),
        name='block-type-list'
    ),
    url(
        r'^pages/select-form$',
        views.PageSelectFormView.as_view(),
        name='pages-select-form'
    ),
    url(
        r'^page/(?P<pk>\d+)/move$',
        views.PageMoveView.as_view(),
        name='page-move'
    ),
)
