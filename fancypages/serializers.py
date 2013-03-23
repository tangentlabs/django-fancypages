from django.template import loader, Context


class HtmlSerializer(object):

    def __init__(self, templates, render_static=False):
        self.templates = templates
        self.render_static = render_static

    def get_context_data(self, **kwargs):
        return kwargs

    def render(self, tile_renderer):
        tmpl = loader.select_template(self.templates)
        context = Context(self.get_context_data(tile=tile_renderer))
        return tmpl.render(context)
