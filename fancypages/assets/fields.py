# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import django
from django.db.models.fields.related import ForeignKey

from .forms import AssetField


class AssetKey(ForeignKey):

    def formfield(self, **kwargs):
        kwargs['form_class'] = AssetField
        return super(AssetKey, self).formfield(**kwargs)

    def value_from_object(self, obj):
        asset_obj = getattr(obj, self.name, None)
        if not asset_obj:
            return None
        return [asset_obj.id, asset_obj._meta.module_name]


# This is only required for Django version < 1.7 suing South for migrations
if django.VERSION[:2] < (1, 7):
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fancypages\.assets\.fields\.AssetKey"])
