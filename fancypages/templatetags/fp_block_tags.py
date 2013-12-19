from django import template
from django.conf import settings
from django.db.models import get_model
from django.template import defaultfilters, loader

from .. import library
from .. import renderers
from ..dashboard import forms

ContentType = get_model('contenttypes', 'ContentType')

register = template.Library()


@register.assignment_tag
def update_blocks_form(page, container_name):
    container = page.get_container_from_name(container_name)
    if not container:
        return None
    return forms.BlockUpdateSelectForm(container)


@register.simple_tag(takes_context=True)
def render_attribute(context, attr_name, *args):
    """
    Render an attribute based on editing mode.
    """
    block = context.get(renderers.BlockRenderer.context_object_name)
    value = getattr(block, attr_name)

    for arg in args:
        flt = getattr(defaultfilters, arg)
        if flt:
            value = flt(value)

    user = context.get('request').user
    if not user.is_authenticated:
        return unicode(value)
    if not user.is_staff:
        return unicode(value)

    wrapped_attr = u'<span id="block-{uuid}-{attr_name}">{value}</span>'
    return wrapped_attr.format(
        uuid=block.uuid, attr_name=attr_name, value=unicode(value))


@register.assignment_tag(takes_context=True)
def get_object_visibility(context, obj):
    try:
        return obj.is_visible
    except AttributeError:
        pass
    return True


@register.simple_tag(takes_context=True)
def render_block_form(context, form):
    model = form._meta.model
    model_name = model.__name__.lower()
    template_names = [
        "%s/%s_form.html" % (model._meta.app_label, model_name),
        "fancypages/blocks/%s_form.html" % model_name, form.template_name]
    tmpl = loader.select_template(template_names)

    context['missing_image_url'] = "%s/%s" % (
        settings.MEDIA_URL, getattr(settings, "OSCAR_MISSING_IMAGE_URL", ''))
    return tmpl.render(context)


@register.filter
def depth_as_range(depth):
    # reduce depth by 1 as treebeard root depth is 1
    return range(depth - 1)


@register.assignment_tag
def get_content_type(obj):
    return ContentType.objects.get_for_model(obj.__class__)


@register.inclusion_tag(
    'fancypages/dashboard/block_select.html', takes_context=True)
def render_block_selection(context):
    request = context.get('request')
    if not request or not request.fp_edit_mode:
        return u''
    grouped_blocks = library.get_grouped_content_blocks()
    return {'grouped_blocks': grouped_blocks}
