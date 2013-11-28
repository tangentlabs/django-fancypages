from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...assets.fields import AssetKey


class MultiImageMeta(models.base.ModelBase):

    def __init__(cls, name, bases, nmspc):
        super(MultiImageMeta, cls).__init__(name, bases, nmspc)
        if hasattr(cls, 'num_images'):
            cls.add_image_fields()

    def add_image_fields(cls):
        if not getattr(cls, 'image_field_name', None):
            cls.image_field_name = "image_%d"

        for idx in range(1, cls.num_images + 1):
            cls.add_to_class(
                cls.image_field_name % idx,
                AssetKey('assets.ImageAsset', verbose_name=_("Image %d" % idx),
                         related_name="+", blank=True, null=True))


class MultiLinkMeta(models.base.ModelBase):

    def __init__(cls, name, bases, nmspc):
        super(MultiLinkMeta, cls).__init__(name, bases, nmspc)
        if hasattr(cls, 'num_links'):
            cls.add_link_fields()

    def add_link_fields(cls):
        if not getattr(cls, 'link_field_name', None):
            cls.link_field_name = "link_url_%d"

        for idx in range(1, cls.num_links + 1):
            cls.add_to_class(
                cls.link_field_name % idx,
                models.CharField(_("Link URL %d" % idx), max_length=500,
                                 blank=True, null=True))


class MultiImageLinkMeta(MultiImageMeta, MultiLinkMeta):
    pass
