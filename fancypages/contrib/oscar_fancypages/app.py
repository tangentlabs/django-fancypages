from __future__ import absolute_import

from django.conf.urls.defaults import patterns, url

from oscar.core.application import Application

from . import views


class OscarFancypagesApplication(Application):
    name = 'fancypages'

    page_detail_view = views.FancyPageDetailView

    def get_urls(self):
        urlpatterns = super(OscarFancypagesApplication, self).get_urls()
        urlpatterns += patterns(
            '',
            url(
                r'^(?P<slug>[\w-]+(/[\w-]+)*)/$',
                self.page_detail_view.as_view(),
                name='page-detail'
            ),
        )
        return self.post_process_urls(urlpatterns)


application = OscarFancypagesApplication()
