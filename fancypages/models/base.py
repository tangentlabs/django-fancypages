from django.db import models

from .. import abstract_models


class PageType(abstract_models.AbstractPageType):
    class Meta:
        app_label = 'fancypages'


class PageGroup(abstract_models.AbstractPageGroup):
    class Meta:
        app_label = 'fancypages'


class PageNode(abstract_models.AbstractPageNode):
    class Meta(abstract_models.AbstractPageNode.Meta):
        swappable = 'FP_NODE_MODEL'


class FancyPage(abstract_models.AbstractFancyPage):
    class Meta(abstract_models.AbstractFancyPage.Meta):
        swappable = 'FP_PAGE_MODEL'


class Container(abstract_models.AbstractContainer):
    class Meta:
        app_label = 'fancypages'
        unique_together = (('name', 'content_type', 'object_id',
                            'language_code'),)


class OrderedContainer(Container):
    display_order = models.PositiveIntegerField()

    @property
    def block_uuid(self):
        """
        Returns the UUID of content block this container is attached to.
        """
        return self.page_object.uuid

    def __unicode__(self):
        return u"Container #{0} '{1}' in '{2}'".format(
            self.display_order, self.name, self.content_type)

    class Meta:
        app_label = 'fancypages'
