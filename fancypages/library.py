from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


_content_blocks = {}


def register_content_block(klass):
    global _content_blocks

    if not klass.code:
        raise ImproperlyConfigured(
            "you have to specify a unique code for this content_block")

    if klass.name is None:
        raise ImproperlyConfigured(
            "you need to specify a name for this widget")

    if klass.code in _content_blocks:
        raise ImproperlyConfigured("a content_block with code {0} is already "
                                   "registered".format(klass.code))

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
        blocks.setdefault(unicode(group), []).append({
            'code': block.code,
            'name': unicode(block.name)
        })
    # we now have to sort the the groups alphabetically
    return SortedDict([(g, blocks[g]) for g in sorted(blocks.keys())])
