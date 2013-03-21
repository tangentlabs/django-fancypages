from django.db import models

from treebeard.mp_tree import MP_Node


class AbstractTreeNode(MP_Node):
    """
    Define the tree structure properties of the fancy page. This is a
    separate abstract class to make sure that it can be easily replaced
    by another tree handling library or none if needed.
    """
    class Meta:
        abstract = True


class AbstractFancyPage(models.Model):
    class Meta:
        abstract = True


class AbstractContainer(models.Model):
    class Meta:
        abstract = True


class AbstractTileModel(models.Model):
    class Meta:
        abstract = True
