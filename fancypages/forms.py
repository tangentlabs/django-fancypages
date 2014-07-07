# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms


class BaseBlockForm(forms.Form):
    next = forms.CharField(widget=forms.HiddenInput())

    def hidden_fields(self):
        """
        Override the default form behaviour to exclude the ``next`` field from
        being added in HTML. It needs to be added manually.
        """
        return [field for field in self
                if field.is_hidden and field.name != 'next']
