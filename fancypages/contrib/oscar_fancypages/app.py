from __future__ import absolute_import

from django.conf import settings
from django.conf.urls.defaults import patterns, url

from oscar.core.application import Application

from . import views
from ...defaults import FP_PAGE_URLPATTERN


class OscarFancypagesApplication(Application):
    FP_PAGE_URLPATTERN = getattr(
        settings, 'FP_PAGE_URLPATTERN', FP_PAGE_URLPATTERN)

    name = 'fancypages'

    page_detail_view = views.FancyPageDetailView

    def get_urls(self):
        urlpatterns = super(OscarFancypagesApplication, self).get_urls()
        urlpatterns += patterns(
            '',
            url(
                self.FP_PAGE_URLPATTERN,
                self.page_detail_view.as_view(),
                name='page-detail'
            ),
        )
        return self.post_process_urls(urlpatterns)


application = OscarFancypagesApplication()
