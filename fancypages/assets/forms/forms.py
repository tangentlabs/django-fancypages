from django import forms
from django.db.models import get_model

ImageAsset = get_model('assets', 'ImageAsset')


class ImageAssetCreateForm(forms.ModelForm):

    class Meta:
        model = ImageAsset
        exclude = ('description', 'creator', 'name')
