from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericRelation

from .content import ContentBlock
from ...library import register_content_block


class LayoutBlock(ContentBlock):
    BOOTSTRAP_MAX_WIDTH = 12
    containers = GenericRelation('fancypages.Container')

    class Meta:
        abstract = True
        app_label = 'fancypages'


@register_content_block
class TabBlock(ContentBlock):
    name = _("Tabbed block")
    code = 'tabbed-block'
    group = _("Layout")
    context_object_name = "widget"
    template_name = "fancypages/widgets/tabbedblockwidget.html"

    tabs = GenericRelation('fancypages.OrderedContainer')

    def save(self, *args, **kwargs):
        super(TabBlock, self).save(*args, **kwargs)
        if not self.tabs.count():
            OrderedContainer.objects.create(page_object=self, display_order=0,
                                            title=_("New Tab"))

    class Meta:
        app_label = 'fancypages'


@register_content_block
class TwoColumnLayoutBlock(LayoutBlock):
    name = _("Two column layout")
    code = 'two-column-layout'
    group = _("Layout")
    template_name = "fancypages/widgets/two_column_layout.html"

    LEFT_WIDTH_CHOICES = [(x, x) for x in range(1, 12)]
    left_width = models.PositiveIntegerField(_("Left Width"), max_length=3,
                                             choices=LEFT_WIDTH_CHOICES,
                                             default=6)

    @property
    def left_span(self):
        """ Returns the bootstrap span class for the left container. """
        return u'span%d' % self.left_width

    @property
    def right_span(self):
        """ Returns the bootstrap span class for the left container. """
        return u'span%d' % (self.BOOTSTRAP_MAX_WIDTH - self.left_width)

    class Meta:
        app_label = 'fancypages'


@register_content_block
class ThreeColumnLayoutBlock(LayoutBlock):
    name = _("Three column layout")
    code = 'three-column-layout'
    group = _("Layout")
    template_name = "fancypages/widgets/three_column_layout.html"

    class Meta:
        app_label = 'fancypages'


@register_content_block
class FourColumnLayoutBlock(LayoutBlock):
    name = _("Four column layout")
    code = 'four-column-layout'
    group = _("Layout")
    template_name = "fancypages/widgets/four_column_layout.html"

    class Meta:
        app_label = 'fancypages'
