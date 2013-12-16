from django.conf import settings
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured

from ..defaults import FP_PAGE_MODEL, FP_NODE_MODEL


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


FP_NODE_MODEL = getattr(settings, 'FP_NODE_MODEL', FP_NODE_MODEL)
FP_PAGE_MODEL = getattr(settings, 'FP_PAGE_MODEL', FP_PAGE_MODEL)


def get_node_model():
    return _get_swappable_model(FP_NODE_MODEL)


def get_page_model():
    return _get_swappable_model(FP_PAGE_MODEL)


from .base import (
    FancyPage,
    PageGroup,
    PageType,
    Container,
    OrderedContainer,
)

from .mixins import (
    ImageMetadataMixin,
    NamedLinkMixin,
)

from .blocks import (
    TabBlock,
    TwoColumnLayoutBlock,
    ThreeColumnLayoutBlock,
    FourColumnLayoutBlock,
    ContentBlock,
    TextBlock,
    TitleTextBlock,
    PageNavigationBlock,
    VideoBlock,
    TwitterBlock
)

# this is required here to make sure that the config is loaded when the
# app is loaded as well
from ..conf import FancyPagesConf
