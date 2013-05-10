from django import template
from django.conf import settings
from django.db.models import get_model
from django.template import defaultfilters, loader

from .. import forms

ContentType = get_model('contenttypes', 'ContentType')

register = template.Library()


@register.assignment_tag
def update_widgets_form(page, container_name):
    container = page.get_container_from_name(container_name)
    if not container:
        return None
    return forms.WidgetUpdateSelectForm(container)


@register.simple_tag(takes_context=True)
def render_attribute(context, attr_name, *args):
    """
    Render an attribute based on editing mode.
    """
    widget = context.get('object')
    value = getattr(widget, attr_name)

    for arg in args:
        flt = getattr(defaultfilters, arg)
        if flt:
            value = flt(value)

    user = context.get('request').user
    if not user.is_authenticated:
        return unicode(value)
    if not user.is_staff:
        return unicode(value)

    wrapped_attr = u'<div id="widget-%d-%s">%s</div>'
    return wrapped_attr % (widget.id, attr_name, unicode(value))


@register.assignment_tag(takes_context=True)
def get_object_visibility(context, obj):
    try:
        return obj.is_visible
    except AttributeError:
        pass
    return True


@register.simple_tag(takes_context=True)
def render_widget_form(context, form):
    model = form._meta.model
    model_name = model.__name__.lower()
    template_names = [
        "%s/%s_form.html" % (model._meta.app_label, model_name),
        "fancypages/widgets/%s_form.html" % model_name,
        form.template_name,
    ]
    tmpl = loader.select_template(template_names)

    context['missing_image_url'] = "%s/%s" % (
        settings.MEDIA_URL,
        getattr(settings, "OSCAR_MISSING_IMAGE_URL", '')
    )
    return tmpl.render(context)


@register.filter
def depth_as_range(depth):
    # reduce depth by 1 as treebeard root depth is 1
    return range(depth-1)


@register.assignment_tag
def get_content_type(obj):
    return ContentType.objects.get_for_model(obj.__class__)


@register.inclusion_tag('fancypages/dashboard/widget_select.html', takes_context=True)
def render_widget_selection(context):
    request = context.get('request')
    if not request or not request.fancypage_edit_mode:
        return u''
    grouped_widgets = get_model('fancypages', 'Widget').get_available_widgets()
    return {
        'container': context['container'],
        'grouped_widgets': grouped_widgets,
    }
