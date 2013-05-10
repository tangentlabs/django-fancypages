from django.http import Http404
from django.conf import settings
from django.views.generic import DetailView

from .models import FancyPage


class PageMixin(object):

    def get_template_names(self):
        if not self.object.page_type:
            return [settings.FANCYPAGES_DEFAULT_TEMPLATE]
        return [self.object.page_type.template_name]


class FancyPageDetailView(PageMixin, DetailView):
    model = FancyPage


class HomeView(PageMixin, DetailView):
    model = FancyPage

    def get(self, request, *args, **kwargs):
        self.kwargs.setdefault('slug', 'home')
        self.object = self.get_object()
        response = super(HomeView, self).get(request, *args, **kwargs)
        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response

    def get_object(self):
        try:
            page = FancyPage.objects.get(slug='home')
        except FancyPage.DoesNotExist:
            page = FancyPage.add_root(title='Home', slug='home')
        return page
