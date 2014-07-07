# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _

from fancypages.forms import BaseBlockForm


class ContactUsForm(BaseBlockForm):
    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Email"))
    message = forms.CharField(label=_("Message"), widget=forms.Textarea())
