from django.db import models

from .queryset import PageQuerySet


class PageManager(models.Manager):

    def get_query_set(self):
        return PageQuerySet(self.model).order_by('path')

    def visible(self, **kwargs):
        return PageQuerySet(self.model).visible(**kwargs)

    def visible_in(self, group):
        return PageQuerySet(self.model).visible_in(group=group)
