from copy import copy

from django import template
from django.template import loader
from django.core.exceptions import ImproperlyConfigured

from .models import ContentBlock, Container


class ContainerRenderer(object):

    def __init__(self, container, context, extra_context=None):
        if not container and not issubclass(container, Container):
            raise TypeError(
                "block must be a subclass of 'ContentBlock' not "
                "'%s'" % type(container)
            )
        if not extra_context:
            extra_context = {}
        self.container = container
        self.context = copy(context)
        self.context.update(extra_context)

    def get_context_data(self, **kwargs):
        return kwargs

    def render(self):
        """
        Render the container and all its contained blocks.
        """
        ordered_blocks = self.container.blocks.select_subclasses()

        tmpl = loader.select_template(self.container.get_template_names())

        rendered_blocks = []
        for block in ordered_blocks:
            renderer = block.get_renderer_class()(block, self.context)
            try:
                rendered_block = renderer.render()
            except ImproperlyConfigured:
                continue
            rendered_blocks.append((block, rendered_block))

        self.context['container'] = self.container
        self.context['rendered_blocks'] = rendered_blocks
        self.context.update(self.get_context_data())
        return tmpl.render(self.context)


class BlockRenderer(object):
    context_object_name = 'fp_block'

    def __init__(self, block, context, extra_context=None):
        if not block and not issubclass(block, ContentBlock):
            raise TypeError(
                "block must be a subclass of 'ContentBlock' not "
                "'%s'" % type(block)
            )
        if not extra_context:
            extra_context = {}
        self.block = block
        self.context = copy(context)
        self.context.update(extra_context)

    def get_context_data(self, **kwargs):
        return kwargs

    def render(self):
        if not self.block.get_template_names():
            raise ImproperlyConfigured(
                "a template name is required for a block to be rendered"
            )
        try:
            tmpl = loader.select_template(self.block.get_template_names())
        except template.TemplateDoesNotExist:
            return u''

        self.context[self.context_object_name] = self.block
        self.context.update(self.get_context_data())
        return tmpl.render(self.context)
