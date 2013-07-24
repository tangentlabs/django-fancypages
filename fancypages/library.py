from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


_content_blocks = {}


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
    registered_blocks = {}
    for block in _content_blocks.values():
        if not block._meta.abstract:
            if not block.name:
                raise ImproperlyConfigured(
                    "a block model has to provide 'name' attributes"
                )
            group = getattr(block, 'group', _('Default'))
            registered_blocks.setdefault(unicode(group), []).append((
                block.code,
                unicode(block.name)
            ))
    return registered_blocks
