from django.db import models
from django.utils.translation import ugettext_lazy as _

from fancypages import abstract_models


class FancyPage(abstract_models.AbstractFancyPage,
                abstract_models.AbstractTreeNode):
    pass


class Container(abstract_models.AbstractContainer):
    pass


class Tile(abstract_models.AbstractTileModel):
    pass


class TextTile(Tile):
    text = models.CharField(_("Text"), max_length=255)

    def __unicode__(self):
        return "Text tile: %s" % self.text
