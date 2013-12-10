import shortuuid

from django.conf.urls import patterns, url

from fancypages.api import views

SHORTUUID_ALPHA = shortuuid.get_alphabet()


urlpatterns = patterns(
    '',
    url(r'^blocks$', views.BlockListView.as_view(), name='block-list'),
    url(
        r'^block/(?P<uuid>[{0}]+)$'.format(SHORTUUID_ALPHA),
        views.BlockDetailView.as_view(),
        name='block-detail'
    ),
    url(
        r'^block/(?P<uuid>[{0}]+)/form$'.format(SHORTUUID_ALPHA),
        views.BlockFormView.as_view(),
        name='block-form'
    ),
    url(
        r'^block/(?P<uuid>[{0}]+)/move$'.format(SHORTUUID_ALPHA),
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
