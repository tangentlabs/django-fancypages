from django import forms

# we can't import the image asset model using get_model because models.py has
# no been loaded at the time the forms module is loaded. We don't want to spend
# any time on investigating workarounds because the asset manager is going to
# be replaced soon anyways.
from ..models import ImageAsset


class ImageAssetCreateForm(forms.ModelForm):

    class Meta:
        model = ImageAsset
        exclude = ('description', 'creator', 'name')
