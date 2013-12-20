from django.conf import settings
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from django.template import loader, TemplateDoesNotExist

from fancypages.templatetags import fp_container_tags

from ..defaults import FP_PAGE_MODEL, FP_NODE_MODEL

FP_NODE_MODEL = getattr(settings, 'FP_NODE_MODEL', FP_NODE_MODEL)
FP_PAGE_MODEL = getattr(settings, 'FP_PAGE_MODEL', FP_PAGE_MODEL)


def _get_swappable_model(name):
    try:
        app_label, model_name = name.split('.')
    except ValueError:
        raise ImproperlyConfigured(
            "{} must be of the form 'app_label.model_name'".format(name))
    model_class = get_model(app_label, model_name)
    if model_class is None:
        raise ImproperlyConfigured(
            "{} refers to model '{}.{}' that has not been installed".format(
                name, app_label, model_name))
    return model_class


def get_node_model():
    return _get_swappable_model(FP_NODE_MODEL)


def get_page_model():
    return _get_swappable_model(FP_PAGE_MODEL)


def get_container_names_from_template(page_template):
    try:
        template_name = page_template.template_name
    except AttributeError:
        template_name = page_template

    container_names = []
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return []

    for node in template:
        container_nodes = node.get_nodes_by_type(
            fp_container_tags.FancyObjectContainerNode
        )

        for cnode in container_nodes:
            var_name = cnode.container_name.var
            if var_name in container_names:
                raise ImproperlyConfigured(
                    "duplicate container name '%s' in template '%s'",
                    var_name,
                    template_name
                )
            container_names.append(var_name)
    return container_names


def loaddata(orm, fixture_name):
    """
    Overwrite the ``_get_model`` command in the serialiser to use the
    FakeORM model from south instead of the latest model.
    """
    from dingus import patch

    _get_model = lambda model_identifier: orm[model_identifier]

    with patch('django.core.serializers.python._get_model', _get_model):
        from django.core.management import call_command
        call_command("loaddata", fixture_name)


try:
    from oscar.core.utils import slugify as unicode_slugify
except ImportError:
    from unidecode import unidecode
    from django.template.defaultfilters import slugify

    def unicode_slugify(value):
        return slugify(unidecode(value))
