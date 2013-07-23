from django.db import models

from .queryset import PageQuerySet


class PageManager(models.Manager):
    def get_query_set(self):
        return PageQuerySet(self.model).order_by('path')
