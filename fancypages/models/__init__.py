from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

from .mixins import *
from .blocks import *
from .. import abstract_models
#from ..utils import get_container_names_from_template

# this is required here to make sure that the config is loaded when the
# app is loaded as well
from ..conf import FancyPagesConf


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
    pass


class VisibilityType(abstract_models.AbstractVisibilityType):
    pass


class FancyPage(abstract_models.AbstractFancyPage,
                abstract_models.AbstractTreeNode):
    objects = PageManager()


class Container(abstract_models.AbstractContainer):
    pass


class OrderedContainer(Container):
    display_order = models.PositiveIntegerField()

    def __unicode__(self):
        return u"Container #%d '%s' in '%s'" % (
            self.display_order,
            self.variable_name,
            self.content_type
        )

    class Meta:
        app_label = 'fancypages'
