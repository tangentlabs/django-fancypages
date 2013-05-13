from django.conf.urls.defaults import patterns, url, include

from ..utils.application import Application
from ..utils.decorators import staff_member_required

from . import views
from ..assets.app import application as assets_app


class FancypagesDashboardApplication(Application):
    name = 'fp-dashboard'
    assets_app = assets_app

    page_list_view = views.PageListView
    page_create_view = views.PageCreateView
    page_update_view = views.PageUpdateView
    page_delete_view = views.PageDeleteView

    block_update_view = views.BlockUpdateView
    block_delete_view = views.BlockDeleteView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^assets/', include(self.assets_app.urls)),

            url(
                r'^$',
                self.page_list_view.as_view(),
                name='page-list'
            ),
            url(
                r'^create/$',
                self.page_create_view.as_view(),
                name='page-create'
            ),
            url(
                r'^create/(?P<parent_pk>\d+)/$',
                self.page_create_view.as_view(),
                name='child-page-create'
            ),
            url(
                r'^update/(?P<pk>\d+)/$',
                self.page_update_view.as_view(),
                name='page-update'
            ),
            url(
                r'^delete/(?P<pk>\d+)/$',
                self.page_delete_view.as_view(),
                name='page-delete'
            ),

            url(
                r'^block/update/(?P<pk>\d+)/$',
                self.block_update_view.as_view(),
                name='block-update'
            ),
            url(
                r'^block/delete/(?P<pk>\d+)/$',
                self.block_delete_view.as_view(),
                name='block-delete'
            ),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = FancypagesDashboardApplication()
