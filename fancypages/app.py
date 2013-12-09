from django.conf.urls import patterns, url

from .utils.application import Application

from fancypages import views


class FancypagesApplication(Application):
    name = 'fancypages'

    page_view = views.FancyPageDetailView

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(r'^(?P<slug>[\w-]+(/[\w-]+)*)/$', self.page_view.as_view(),
                name='page-detail'))
        return self.post_process_urls(urlpatterns)


application = FancypagesApplication()
