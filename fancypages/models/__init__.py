from django.db import models
from django.utils.translation import ugettext_lazy as _

from fancypages import abstract_models


class FancyPage(abstract_models.AbstractFancyPage,
                abstract_models.AbstractTreeNode):
    pass


class Container(abstract_models.AbstractContainer):
    pass


class TileModel(abstract_models.AbstractTileModel):
    pass


class TextTileModel(TileModel):
    text = models.CharField(_("Text"), max_length=255)
