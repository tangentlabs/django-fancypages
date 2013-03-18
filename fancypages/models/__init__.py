from django.db import models
from django.utils.translation import ugettext_lazy as _

from fancypages import abstract_models


class FancyPage(abstract_models.AbstractFancyPage):
    pass


class Container(abstract_models.AbstractContainer):
    pass


class WidgetModel(abstract_models.AbstractWidgetModel):
    pass


class TextWidgetModel(WidgetModel):
    text = models.CharField(_("Text"), max_length=255)
