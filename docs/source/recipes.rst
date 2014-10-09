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


Changing Rich Text Editor
-------------------------

Fancypages uses `Trumbowyg`_ as the rich text editor by default. It is an
open-source tool licensed under the MIT license and provides the basics
required for rich text editing in the fancypages editor panel.

Alternatively, other rich text editors can be used instead. Fancypages comes
with an alternative setup for `Froala`_. Although Froala is a more
comprehensive editor, it is not the default because of its license. It is only
free to use for personal and non-profit project, commercial projects require
a license.


Switching to Froala
~~~~~~~~~~~~~~~~~~~

The Froala editor can be enabled in three simple steps but before we get
started, you have to `download Froala`_ from their website and unpack it.

**Step 1:** Copy the files ``froala_editor.min.js`` and
``froala_editor.min.css`` into your project's static file directory. This would
usually be something like ``static/libs/froala/``.

**Step 2:** Override the fancypages partials that define JavaScript and CSS
files required to the editor panel. Copy the following three files from
fancypages into your template directory::

    templates/fancypages/editor/head.html
    templates/fancypages/editor/partials/cdn_scripts.html
    templates/fancypages/editor/partials/extrascripts.html

Remove the ``trumbowyg.css`` and ``trumbowyg.min.js`` files forom the
``head.html`` and ``extrascripts.html`` respectively and replace them with
the corresponding CSS and JavaScript files for Froala. You'll also need to
add `Font Awesome`_ to the ``cdn_scripts.html``, e.g.:

.. code-block:: html

    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
    

**Step 3:** Set the rich text editor to ``Froala`` when initialising the
Fancypages app in the editor panel by overwriting
``templates/fancypages/editor/body.html`` and starting the application using:

.. code-block:: javascript

    $(document).ready(function(){
        FancypageApp.start({'editor': 'froala'});
    });

The rich text editors in the editor panel should now use Froala instead of the
default Trumbowyg editor.


.. _`Trumbowyg`: http://alex-d.github.io/Trumbowyg
.. _`Froala`: http://editor.froala.com/
.. _`download Froala`: http://editor.froala.com/download
.. _`Font Awesome`: http://fortawesome.github.io/Font-Awesome/


Using a custom editor
~~~~~~~~~~~~~~~~~~~~~

You can also use your favourite editor by adding all the JavaScript and CSS
requirements similar to the Froala example and providing a Backbone/Marionette
view class that provides the necessary initialisations. For an example, take a
look at the ``FroalaEditor`` and ``TrumbowygEditor`` views in `the Marionette
views for Fancypages`_. To enable your editor set the ``editor`` option
for the Fancypages app to ``custom`` and pass you view class as the
``editorView``. An example might look like this:

.. code-block:: javascript

    $(document).ready(function(){
        FancypageApp.start({
            editor: 'custom',
            editorView: myownjavascript.Views.FavouriteEditor
        });
    });
    

.. _`the Marionette views for Fancypages`: https://github.com/tangentlabs/django-fancypages/blob/master/fancypages/static/fancypages/src/js/views.js


Customising Rich Text Editor
----------------------------

In addition to choose the editor you want to use for rich text editing, you can
also configure the way the editor behaves by passing editor-specific options
to the fancypages app when it is initialised in the
``fancypages/editor/body.html`` template. Simply overwrite the template and
update the script section at the bottom with something like this::

.. code-block:: javascript

    $(document).ready(function(){
        FancypageApp.start({
            editor: 'trumbowyg',
            editorOptions: {
                fullscreenable: true
                btns: [
                    'viewHTML',
                    '|', 'formatting',
                    '|', 'link',
                    '|', 'insertImage',
                    '|', 'insertHorizontalRule'
                ]
            },
        });
    });
