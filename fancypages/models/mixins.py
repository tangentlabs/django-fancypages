from django.db import models
from django.utils.translation import ugettext_lazy as _


class ImageMetadataMixin(models.Model):
    """
    Mixin for meta data for image widgets
    """
    title = models.CharField(_("Image title"), max_length=100, blank=True,
                             null=True)
    alt_text = models.CharField(_("Alternative text"), max_length=100,
                                blank=True, null=True)
    link = models.CharField(_("Link URL"), max_length=500, blank=True,
                            null=True)

    class Meta:
        abstract = True
        app_label = 'fancypages'


class NamedLinkMixin(models.Model):
    """
    Mixin providing a link field and a field to name that link in the
    widget.
    """
    link = models.CharField(_("Link"), max_length=255, null=True, blank=True)
    link_title = models.CharField(_("Link title"), max_length=255, null=True,
                                  blank=True, default="Read more")

    class Meta:
        abstract = True
        app_label = 'fancypages'
