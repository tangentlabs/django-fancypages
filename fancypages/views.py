# -*- coding: utf-8- -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic import DetailView

from . import mixins
from .utils import get_page_model


class FancyPageDetailView(mixins.FancyPageMixin, DetailView):
    slug_field = 'node__slug'


class HomeView(mixins.FancyHomeMixin, DetailView):
    content_object_name = 'fancypage'

    def get_queryset(self):
        return get_page_model()._default_manager.all()
