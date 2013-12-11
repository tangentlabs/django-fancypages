from django.db import models

from .. import abstract_models
from ..manager import PageManager


class PageType(abstract_models.AbstractPageType):
    class Meta:
        app_label = 'fancypages'


class PageGroup(abstract_models.AbstractPageGroup):
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
        unique_together = (('name', 'content_type', 'object_id'),)


class OrderedContainer(Container):
    display_order = models.PositiveIntegerField()

    @property
    def block_uuid(self):
        return self.page_object.uuid

    def __unicode__(self):
        return u"Container #{0} '{1}' in '{2}'".format(
            self.display_order,
            self.name,
            self.content_type
        )

    class Meta:
        app_label = 'fancypages'
