from django.conf.urls.defaults import patterns, url

from fancypages.api import views


urlpatterns = patterns('',
    url(r'^$', views.ApiV1View.as_view(), name="api-root"),
    url(r'^widgets$', views.WidgetListView.as_view(), name='widget-list'),
    url(
        r'^widget/(?P<pk>\d+)$',
        views.WidgetRetrieveUpdateDestroyView.as_view(),
        name='widget-retrieve-update-destroy'
    ),
    url(
        r'^widget/(?P<pk>\d+)/move$',
        views.WidgetMoveView.as_view(),
        name='widget-move'
    ),
    url(
        r'^ordered-containers$',
        views.OrderedContainerListView.as_view(),
        name='ordered-container-list'
    ),
    url(
        r'^widget-types$',
        views.WidgetTypesView.as_view(),
        name='widget-type-list'
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
