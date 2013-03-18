from django.db import models

from .widgets import Widget

__widgets = {}


def itersubclasses(cls, _seen=None):
    """
    I have taken this method from:

    http://code.activestate.com/recipes/576949-find-all-subclasses-of-a-given-class/

    so that I don't have to do this all myself :)
    """
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
                        'new-style classes, not %.100r' % cls)
    if _seen is None:
        _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError:  # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub


if not __widgets:
    for widget_class in itersubclasses(Widget):
        if not issubclass(widget_class.model, models.Model):
            raise Exception('you need to specify a model for widget')
        if widget_class.model in __widgets:
            raise Exception('widget for model already registered')
        __widgets[widget_class.model.__name__] = widget_class


def get_widget_for_model(model):
    try:
        return __widgets[model.__class__.__name__]
    except KeyError:
        pass
    try:
        return __widgets[model.__name__]
    except KeyError:
        pass
    return None

