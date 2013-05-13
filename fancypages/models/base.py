from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

from .. import abstract_models


class PageQuerySet(QuerySet):

    def visible(self):
        now = timezone.now()
        return self.filter(
            status=FancyPage.PUBLISHED
        ).filter(
            models.Q(date_visible_start=None) |
            models.Q(date_visible_start__lt=now),
            models.Q(date_visible_end=None) |
            models.Q(date_visible_end__gt=now)
        )

    def visible_in(self, visibility_type):
        return self.visible().filter(visibility_types=visibility_type)


class PageManager(models.Manager):
    def get_query_set(self):
        return PageQuerySet(self.model).order_by('path')


class PageType(abstract_models.AbstractPageType):
    class Meta:
        app_label = 'fancypages'


class VisibilityType(abstract_models.AbstractVisibilityType):
    class Meta:
        app_label = 'fancypages'


class FancyPage(abstract_models.AbstractTreeNode,
                abstract_models.AbstractFancyPage):
    objects = PageManager()

    class Meta:
        app_label = 'fancypages'


class Container(abstract_models.AbstractContainer):
    class Meta:
        app_label = 'fancypages'


class OrderedContainer(abstract_models.AbstractContainer):
    display_order = models.PositiveIntegerField()

    def __unicode__(self):
        return u"Container #%d '%s' in '%s'" % (
            self.display_order,
            self.variable_name,
            self.content_type
        )

    class Meta:
        app_label = 'fancypages'
