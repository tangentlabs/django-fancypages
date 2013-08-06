=======
Recipes
=======

Create a Custom Template Block
------------------------------

Start off by creating a new app in your project, e.g. a ``blocks`` app. Conent
blocks in fancypages are basically Django models that require a few additional
attributes and definitions.

Let's assume we want to create a simple widget that displays a custom template
without providing any additional data that can be edited. All we need to do is
define the following model::

    from fancypages.models.blocks import ContentBlock
    from fancypages.library import register_content_block

    @register_content_block
    class MyTemplateBlock(ContentBlock):
        name = _("My template")
        code = u'my-template'
        group = u'My Blocks'
        template_name = u'blocks/my_template_block.html'

        def __unicode__(self):
            return self.name

The first three attributes ``name``, ``code`` and ``group`` are important and
have to be specified on every new content block.

+-----------+---------------------------------------------------------+
| ``name``  | Display name of the content block                       |
+-----------+---------------------------------------------------------+
| ``code``  | **Unique** code for the block to be identified by       |
+-----------+---------------------------------------------------------+
| ``group`` | Blocks can be grouped by using the same group name here |
+-----------+---------------------------------------------------------+
