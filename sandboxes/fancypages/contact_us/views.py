# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views import generic
from django.contrib import messages

from .forms import ContactUsForm


class ContactUsView(generic.FormView):
    form_class = ContactUsForm
    template_name = "contact_us/contact_us_form.html"

    def form_valid(self, form):
        self.success_url = form.cleaned_data.get('next', '/')
        messages.info(
            self.request,
            "Thanks for getting in touch. We'll respond as quickly as we can")
        return super(ContactUsView, self).form_valid(form)
