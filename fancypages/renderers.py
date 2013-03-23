from django.template import loader, Context
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from . import models


class BaseTileRenderer(object):
    model = None
    name = None
    group = None
    # form used for editing, might be
    # the wrong place here
    form_class = None
    serializer = None
    template_name = None
    enable_static_rendering = False

    def __init__(self, tile):
        self.tile = tile

    def get_serializer(self):
        return self.serializer(
            self.get_template_names(),
            self.enable_static_rendering,
        )

    def get_model(self):
        return self.model

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        group_folder = u''
        if self.group:
            group_folder = "%s/" % str(slugify(self.group))
        return ["fancypages/tiles/%s%s.html" % (group_folder, self.model._meta.module_name)]

    def __getitem__(self, item):
        if hasattr(self.tile, item):
            content = getattr(self.tile, item)
            tmpl = loader.get_template('fancypages/tiles/attribute.html')
            return tmpl.render(Context({
                'attribute_name': item,
                'attribute_content': content,
            }))
        return u''

    def __setitem__(self, item, value):
        model = self.get_model()
        if hasattr(model, item):
            raise AttributeError('cannot set value on model attribute')
        raise KeyError("%s has no attribute %s" % (self.model.__class__, item))

    def render(self):
        return self.get_serializer().render(self)


class TextTileRenderer(BaseTileRenderer):
    model = models.TextTile
    name = _("Text")
    code = "text-tile"
    group = _("Content")
