from .base import (
    FancyPage,
    VisibilityType,
    PageType,
    Container,
    OrderedContainer,
)
from .mixins import *
from .blocks import *

# this is required here to make sure that the config is loaded when the
# app is loaded as well
from ..conf import FancyPagesConf
