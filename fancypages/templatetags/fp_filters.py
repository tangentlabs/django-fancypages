from django import template

from ..utils import unicode_slugify

register = template.Library()


@register.filter
def fp_slugify(value):
    """
    Extends the default ``slugify`` filter provided in Django to work with
    non-Ascii characters. The slugify function used uses ``unidecode`` before
    applying the default slugifier. If Oscar is installed, however, the more
    sophisticated slugifier in ``oscar.core.utils`` is used and the
    ``OSCAR_SLUG_MAP`` and ``OSCAR_SLUG_BLACKLIST`` are both respected.
    """
    return unicode_slugify(value)
