from django.conf.urls import patterns, url

from ..utils.application import Application
from ..utils.decorators import staff_member_required

from . import views


class AssetApplication(Application):
    name = None

    image_list_view = views.ImageListView
    image_asset_create_view = views.ImageAssetCreateView

    def get_urls(self):
        urlpatterns = super(AssetApplication, self).get_urls()

        urlpatterns += patterns(
            '',
            url(
                r'^images/$',
                self.image_list_view.as_view(),
                name='image-list'
            ),
            url(
                r'^image/upload/$',
                self.image_asset_create_view.as_view(),
                name='image-upload'
            ),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = AssetApplication()
