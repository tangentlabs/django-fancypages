from django.conf import settings
from django.conf.urls import patterns, url

from . import views
from .defaults import FP_PAGE_URLPATTERN
from .utils.application import Application


class FancypagesApplication(Application):
    FP_PAGE_URLPATTERN = getattr(
        settings, 'FP_PAGE_URLPATTERN', FP_PAGE_URLPATTERN)

    name = 'fancypages'

    page_view = views.FancyPageDetailView

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(
                self.FP_PAGE_URLPATTERN,
                self.page_view.as_view(),
                name='page-detail'
            )
        )
        return self.post_process_urls(urlpatterns)


application = FancypagesApplication()
