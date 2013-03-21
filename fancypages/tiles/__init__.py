from .. import models


class Tile(object):
    model = None
    renderer_class = None
    form_class = None
    template_name = None
    # specifies if the content of the widget can be rendered
    # into static html after model is saved to database
    static_content = False

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        return ["fancypages/widgets/%s" % self.model._meta.module_name]


class TextWidget(Tile):
    model = models.TextWidgetModel
