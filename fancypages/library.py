from __future__ import absolute_import

import logging

from django.forms.models import modelform_factory
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from fancypages.compat.loading import import_string

logger = logging.getLogger('fancypages')


_content_blocks = {}
_block_forms = {}
_imported_form_cache = {}


def register_block_form(model, form):
    global _block_forms, _imported_form_cache

    try:
        model_name = model.__name__
    except AttributeError:
        raise ImproperlyConfigured(
            "{} doesn't appear to be a valid model", )

    if model_name not in _block_forms:
        try:
            module, klass = form.__module__, form.__name__
            form_path = '{}.{}'.format(module, klass)
            _imported_form_cache[form_path] = form
        except AttributeError:
            form_path = form

        _block_forms[model_name] = form_path


def get_block_form(model):
    global _imported_form_cache

    try:
        model_name = model.__name__
    except AttributeError:
        raise ImproperlyConfigured(
            "{} doesn't appear to be a valid model", )

    logger.debug("Using model name '{}'".format(model_name))

    if model_name in _imported_form_cache:
        form_class = _imported_form_cache[model_name]
        logger.debug(
            'Found form for {} in import cache. Returning {}'.format(
                model.__name__, form_class))
        return form_class

    if model_name in _block_forms:
        form_class = import_string(_block_forms[model_name])
        if hasattr(form_class, 'Meta') \
           and not getattr(form_class.Meta, 'model', None):
            form_class.Meta.model = model
        logger.debug(
            "Found registered form '{}' for model '{}'".format(
                form_class.__name__, model.__name__))
        _imported_form_cache[model_name] = form_class
        return _imported_form_cache[model_name]

    get_form_class = getattr(model, 'get_form_class')
    if get_form_class and get_form_class():
        form_class = get_form_class()
    else:
        from fancypages.dashboard import forms
        form_class = getattr(forms, '{0}Form'.format(model.__name__), None)
        if not form_class:
            form_class = modelform_factory(model, form=forms.BlockForm)

    if hasattr(form_class, 'Meta') \
       and not getattr(form_class.Meta, 'model', None):
        form_class.Meta.model = model

    _imported_form_cache[model_name] = form_class
    return _imported_form_cache[model_name]


def register_content_block(klass):
    global _content_blocks

    if not klass.code:
        raise ImproperlyConfigured(
            _("you have to specify a unique code for this content_block")
        )
    if not klass.name:
        raise ImproperlyConfigured(
            _("you need to specify a name for this widget")
        )
    if klass.code in _content_blocks:
        raise ImproperlyConfigured(
            _("a content_block with code {0} is already "
              "registered").format(klass.code)
        )
    _content_blocks[klass.code] = klass
    return klass


def unregister_content_block(klass):
    """
    Unregister the content_block *klass* if it has been registered before.
    """
    global _content_blocks
    if klass.code in _content_blocks:
        del _content_blocks[klass.code]


def get_content_blocks():
    return _content_blocks


def get_content_block(code):
    return _content_blocks.get(code, None)


def get_grouped_content_blocks():
    blocks = {}
    for block in _content_blocks.values():
        if block._meta.abstract:
            continue
        if not block.name or not block.code:
            raise ImproperlyConfigured(
                "a block model has to provide a 'name' and 'code' attributes"
            )
        group = getattr(block, 'group', _('Ungrouped'))
        blocks.setdefault(unicode(group), []).append((
            block.code,
            unicode(block.name)
        ))
    # we now have to sort the the groups alphabetically
    return SortedDict([(g, blocks[g]) for g in sorted(blocks.keys())])
