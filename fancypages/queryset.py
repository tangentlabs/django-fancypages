from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet


class PageQuerySet(QuerySet):

    def visible(self, **kwargs):
        now = timezone.now()
        return self.filter(
            status=self.model.PUBLISHED
        ).filter(
            models.Q(date_visible_start=None) |
            models.Q(date_visible_start__lt=now),
            models.Q(date_visible_end=None) |
            models.Q(date_visible_end__gt=now)
        ).filter(**kwargs)

    def visible_in(self, group):
        return self.visible(groups=group)
