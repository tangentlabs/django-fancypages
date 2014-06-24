import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ... import abstract_models
from .base import MultiImageLinkMeta
from ...assets.fields import AssetKey
from ..mixins import ImageMetadataMixin
from ...library import register_content_block


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
            return u"Image '%s'" % os.path.basename(
                self.image_asset.image.path
            )
        return u"Image #%s" % self.id

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
        blank=True,
        null=True,
    )
    text = models.TextField(_("Text"), default=_("Your text goes here."))

    def __unicode__(self):
        if self.image_asset:
            return u"Image with text '{0}'".format(
                os.path.basename(self.image_asset.image.path)
            )
        return u"Image with text #{0}".format(self.id)

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
        return u"Carousel #%s" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class PageNavigationBlock(ContentBlock):
    name = _("Page Navigation")
    code = 'page-navigation'
    group = _("Content")
    template_name = "fancypages/blocks/page_navigation_block.html"

    depth = models.PositiveIntegerField(
        _("Navigation depth"),
        default=2,
    )

    is_relative = models.BooleanField(
        _("Is navigation relative to this page?"),
        default=False,
    )

    def clean(self):
        if self.depth < 1:
            raise ValidationError(
                _("Navigation depth has to be greater than 0")
            )

    def __unicode__(self):
        if self.is_relative:
            return u'Relative page navigation'
        return u'Page Navigation'

    class Meta:
        app_label = 'fancypages'
