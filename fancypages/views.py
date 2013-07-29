from django.http import Http404
from django.db.models import get_model
from django.views.generic import DetailView

from . import mixins

FancyPage = get_model('fancypages', 'FancyPage')


class FancyPageDetailView(mixins.FancyPageMixin, DetailView):
    model = FancyPage
    content_object_name = 'fancypage'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super(FancyPageDetailView, self).get(request, *args,
                                                        **kwargs)
        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404
        return response


class HomeView(mixins.FancyHomeMixin, DetailView):
    model = FancyPage
    content_object_name = 'fancypage'
