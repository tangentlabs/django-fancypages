from django.conf import settings
from django.conf.urls import patterns, url
from django.utils.module_loading import import_by_path

from .defaults import FP_PAGE_URLPATTERN, FP_PAGE_DETAIL_VIEW
from .utils.application import Application


class FancypagesApplication(Application):
    FP_PAGE_URLPATTERN = getattr(
        settings, 'FP_PAGE_URLPATTERN', FP_PAGE_URLPATTERN)

    name = 'fancypages'
    page_view = import_by_path(
        getattr(settings, 'FP_PAGE_DETAIL_VIEW', FP_PAGE_DETAIL_VIEW))

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(
                FP_PAGE_URLPATTERN,
                self.page_view.as_view(),
                name='page-detail'
            )
        )
        return self.post_process_urls(urlpatterns)


application = FancypagesApplication()
