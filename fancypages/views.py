from django.views.generic import DetailView

from . import mixins
from .utils import get_page_model

FancyPage = get_page_model()


class FancyPageDetailView(mixins.FancyPageMixin, DetailView):
    slug_field = 'node__slug'


class HomeView(mixins.FancyHomeMixin, DetailView):
    model = FancyPage
    content_object_name = 'fancypage'
