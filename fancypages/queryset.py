from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet


class PageQuerySet(QuerySet):

    def visible(self):
        now = timezone.now()
        return self.filter(
            status=self.model.PUBLISHED
        ).filter(
            models.Q(date_visible_start=None) |
            models.Q(date_visible_start__lt=now),
            models.Q(date_visible_end=None) |
            models.Q(date_visible_end__gt=now)
        )

    def visible_in(self, visibility_type):
        return self.visible().filter(visibility_types=visibility_type)
