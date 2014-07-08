==============
Content Blocks
==============



Form Block
----------

Generating freely configurable form on the front-end is difficult to get right
and usually has drawbacks in terms of validation of the content that is passed
through. The form block in FP provides a more restrictive way of defining form
by only allowing pre-configurated forms to be selected. All available forms
are configurated as settings and can be selected when editing the form block.


Defining Selectable Forms
~~~~~~~~~~~~~~~~~~~~~~~~~

The `FormBlock <fancypages.models.blocks.content.FormBlock>` uses a setting
named ``FP_FORM_BLOCK_CHOICES`` to specify all available forms with their
respective *action* URLs and (optionally) a template to render the form. An
example would be:

.. code-block:: python

    FP_FORM_BLOCK_CHOICES = {
        'contact-us': {
            'name': "Contact Us Form",
            'form': 'contact_us.forms.ContactUsForm',
            'url': 'contact-us',
            'template_name': 'contact_us/contact_us_form.html',
        }
    }

The key ``contact-us`` is the unique identifier used to store the form used
in a form block. This value will be stored on the block model. Each of the keys
has to provide at least ``name``, ``form`` and ``url`` in its configuration.

+----------+------------------------------------------------------------------+
| ``name`` | | The name displayed in the form block selection.                |
+----------+------------------------------------------------------------------+
| ``form`` | | Dotted path to a form class subclassing                        |
|          | | ``fancypages.form.BaseBlockForm``.                             |
+----------+------------------------------------------------------------------+
| ``url``  | | The URL used in th``action`` attribute of the form. This can   |
|          | | be a Django URL pattnern name that can be used in ``reverse``  |
|          | | or a fully qualified URL including a valid scheme.             |
+----------+------------------------------------------------------------------+

In addition to these mandatory options, a ``template_name`` can be specified
that will be used instead of the default form template 
``fancypages/templates/fancypages/blocks/formblock.html``.
