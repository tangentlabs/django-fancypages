from .. import models

class Widget(object):
    model = None
    renderer_class = None
    form_class = None
    template_name = None

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        return ["fancypages/widgets/%s" % self.model._meta.module_name]


class TextWidget(Widget):
    model = models.TextWidgetModel
