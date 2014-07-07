# -*- coding: utf-8- -*-
from __future__ import absolute_import, unicode_literals

import os
import logging

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ... import abstract_models
from .base import MultiImageLinkMeta
from ...assets.fields import AssetKey
from ..mixins import ImageMetadataMixin
from ...library import register_content_block
from ...helpers import BlockFormSettings

logger = logging.getLogger('fancypages')


class ContentBlock(abstract_models.AbstractContentBlock):
    class Meta:
        ordering = ['display_order']
        app_label = 'fancypages'


@register_content_block
class TextBlock(ContentBlock):
    name = _("Text")
    code = 'text'
    group = _("Content")
    template_name = "fancypages/blocks/textblock.html"

    text = models.TextField(_("Text"), default="Your text goes here.")

    def __unicode__(self):
        return self.text[:20]

    class Meta:
        app_label = 'fancypages'


@register_content_block
class TitleTextBlock(ContentBlock):
    name = _("Title and text")
    code = 'title-text'
    group = _("Content")
    template_name = "fancypages/blocks/titletextblock.html"

    title = models.CharField(_("Title"), max_length=100,
                             default="Your title goes here.")
    text = models.TextField(_("Text"), default="Your text goes here.")

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'fancypages'


@register_content_block
class ImageBlock(ImageMetadataMixin, ContentBlock):
    name = _("Image")
    code = 'image'
    group = _("Content")
    template_name = "fancypages/blocks/imageblock.html"

    image_asset = AssetKey('assets.ImageAsset', verbose_name=_("Image asset"),
                           related_name="image_blocks", blank=True, null=True)

    def __unicode__(self):
        if self.image_asset:
            return "Image '%s'" % os.path.basename(
                self.image_asset.image.path
            )
        return "Image #%s" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class ImageAndTextBlock(ImageMetadataMixin, ContentBlock):
    name = _("Image and text")
    code = 'image-text'
    group = _("Content")
    template_name = "fancypages/blocks/imageandtextblock.html"

    image_asset = AssetKey(
        'assets.ImageAsset',
        verbose_name=_("Image asset"),
        related_name="image_text_blocks",
        blank=True, null=True)

    text = models.TextField(_("Text"), default=_("Your text goes here."))

    def __unicode__(self):
        if self.image_asset:
            return "Image with text '{0}'".format(
                os.path.basename(self.image_asset.image.path)
            )
        return "Image with text #{0}".format(self.id)

    class Meta:
        app_label = 'fancypages'


@register_content_block
class CarouselBlock(ContentBlock):
    __metaclass__ = MultiImageLinkMeta

    name = _("Image carousel")
    code = 'carousel'
    group = _("Content")
    num_images = num_links = 10
    template_name = "fancypages/blocks/carouselblock.html"

    def get_images_and_links(self):
        results = {}
        query = models.Q()
        for idx in range(1, self.num_images + 1):
            image_id = getattr(self, "%s_id" % (self.image_field_name % idx))
            link_field_name = self.link_field_name % idx
            if image_id:
                results[image_id] = {
                    'link': getattr(self, link_field_name, None)
                }
                query.add(models.Q(id=image_id), models.Q.OR)
        if not query:
            return {}

        ImageAsset = models.get_model('assets', 'ImageAsset')
        for image in ImageAsset.objects.filter(query):
            results[image.id]['image'] = image
        return results

    def __unicode__(self):
        return "Carousel #%s" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class PageNavigationBlock(ContentBlock):
    name = _("Page Navigation")
    code = 'page-navigation'
    group = _("Content")
    template_name = "fancypages/blocks/page_navigation_block.html"

    ABSOLUTE = 'absolute'
    RELATIVE_FROM_SIBLINGS = 'relative-siblings'
    RELATIVE_FROM_CHILDREN = 'relative-children'

    ORIGIN_CHOICES = (
        (ABSOLUTE, _("Start from top-level pages")),
        (RELATIVE_FROM_SIBLINGS, _("Start from siblings")),
        (RELATIVE_FROM_CHILDREN, _("Start from children")),
    )

    depth = models.PositiveIntegerField(_("Navigation depth"), default=2)
    origin = models.CharField(
        _("navigation origin"), max_length=50, choices=ORIGIN_CHOICES,
        default=ABSOLUTE)

    def clean(self):
        if self.depth < 1:
            raise ValidationError(
                _("Navigation depth has to be greater than 0"))

    def get_page_tree(self, fancypage):
        from ...templatetags.fp_sitemap_tags import get_page_tree
        relative_to = None

        # if the page object passed in is not defined, we can't do anything
        # sensible to return the "right" thing. So we just return nothing.
        if not fancypage:
            logger.info(
                'requested page tree without fancypage in block {}'.format(
                    self.uuid))
            return []

        if self.origin == self.RELATIVE_FROM_CHILDREN:
            relative_to = fancypage
        elif self.origin == self.RELATIVE_FROM_SIBLINGS:
            relative_to = fancypage.get_parent()

        return get_page_tree(depth=self.depth, relative_to=relative_to)

    def __unicode__(self):
        return 'Page navigation from {}'.format(self.origin)

    class Meta:
        app_label = 'fancypages'


@register_content_block
class FormBlock(ContentBlock):
    name = _("Form")
    code = 'form'
    group = _("Content")

    form_settings = BlockFormSettings()
    form_selection = models.CharField(
        _("form selection"), max_length=255, blank=True,
        choices=form_settings.as_choices())

    class Meta:
        app_label = 'fancypages'

    @property
    def template_name(self):
        default = "fancypages/blocks/formblock.html"
        try:
            conf = self.form_settings[self.form_selection]
        except KeyError:
            return default
        return conf.get('template_name', default)

    @property
    def url(self):
        try:
            url = self.form_settings.get_url(self.form_selection)
        except KeyError:
            return ''
        return url

    @property
    def form(self):
        if not self.form_selection:
            return
        try:
            form = self.form_settings.get_form_class(self.form_selection)
        except KeyError:
            return
        return form()
