from django.forms.models import modelform_factory
from django.template.loader import render_to_string

from rest_framework.renderers import HTMLFormRenderer

from fancypages.dashboard import forms


class BlockFormRenderer(HTMLFormRenderer):
    template_name = "fancypages/dashboard/block_update.html"

    def get_form_class(self):
        model = self.object.__class__
        get_form_class = getattr(model, 'get_form_class')
        if get_form_class and get_form_class():
            return modelform_factory(model, form=get_form_class())

        form_class = getattr(
            forms, "%sForm" % model.__name__, forms.BlockForm)
        return modelform_factory(model, form=form_class)

    def render(self, data, media_type=None, renderer_context=None):
        if not renderer_context:
            return ''

        self.object = renderer_context.get('view').object
        form = self.get_form_class()(
            data=renderer_context.get('request').POST or None,
            instance=self.object)
        context = {'form': form, 'block': self.object}
        return render_to_string(
            self.template_name, context).encode(self.charset)
