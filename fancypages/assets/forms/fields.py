from django.forms import ModelChoiceField

from .widgets import AssetWidget


class AssetField(ModelChoiceField):
    widget = AssetWidget
