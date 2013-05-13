from django.db.models import get_model
from django.template import loader, Context
from django.utils.safestring import mark_safe
from django.forms.widgets import MultiWidget, HiddenInput


class AssetWidget(MultiWidget):
    _delimiter = ':'
    template_name = 'fancypages/assets/forms/asset_widget.html'

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (HiddenInput(), HiddenInput())
        self.widget_id_suffixes = ('id', 'type')
        super(AssetWidget, self).__init__(widgets, attrs)

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(self.get_widget_id(name, i), widget_value, final_attrs))
        rendered_widgets = mark_safe(self.format_output(output))
        tmpl = loader.get_template(self.template_name)
        return tmpl.render(Context({
            'rendered_widgets': rendered_widgets,
            'asset': self.get_asset(*value),
        }))

    def get_widget_id (self, name, idx):
        return "%s_%s" % (name, self.widget_id_suffixes[idx])

    def value_from_datadict(self, data, files, name):
        values = []
        for idx, widget in enumerate(self.widgets):
            widget_name = self.get_widget_id(name, idx)
            values.append(widget.value_from_datadict(data, files, widget_name))
        return values

    def get_asset(self, pk, asset_type):
        if not pk or not asset_type:
            return None
        model = get_model('assets', asset_type)
        try:
            asset = model.objects.get(id=pk)
        except model.DoesNotExist:
            asset = None
        return asset

    def decompress(self, value):
        if value:
            return value
        return [None, None]
