from django.core import validators
from django.db.models import get_model
from django.forms.fields import MultiValueField, CharField, IntegerField

from .widgets import AssetWidget


class AssetField(MultiValueField):
    _delimiter = ':'
    widget = AssetWidget
    default_fields = {
        'asset_pk': IntegerField,
        'asset_type': CharField,
    }

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        self.pk_field_name = kwargs.pop('to_field_name')
        fields = (
            self.default_fields['asset_pk'](),
            self.default_fields['asset_type'](),
        )
        super(AssetField, self).__init__(fields, *args, **kwargs)

    def prepare_value(self, value):
        return super(AssetField, self).prepare_value(value)

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None

        asset_pk, asset_type = value
        model = get_model('assets', asset_type)
        filters = {
            self.pk_field_name: value[0]
        }
        try:
            return model.objects.get(**filters)
        except model.DoesNotExist:
            return None

    def compress(self, data_list):
        return self.to_python(data_list)
