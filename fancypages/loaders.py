from django.db import models

#from .renderers import BaseTileRenderer

#__tiles = {}
#
#
#def itersubclasses(cls, _seen=None):
#    """
#    I have taken this method from:
#
#    http://code.activestate.com/recipes/576949-find-all-subclasses-of-a-given-class/
#
#    so that I don't have to do this all myself :)
#    """
#    if not isinstance(cls, type):
#        raise TypeError('itersubclasses must be called with '
#                        'new-style classes, not %.100r' % cls)
#    if _seen is None:
#        _seen = set()
#    try:
#        subs = cls.__subclasses__()
#    except TypeError:  # fails only when cls is type
#        subs = cls.__subclasses__(cls)
#    for sub in subs:
#        if sub not in _seen:
#            _seen.add(sub)
#            yield sub
#            for sub in itersubclasses(sub, _seen):
#                yield sub
#
#
#if not __tiles:
#    for tile_class in itersubclasses(BaseTileRenderer):
#        if not issubclass(tile_class.model, models.Model):
#            raise Exception('you need to specify a model for tile')
#        if tile_class.model in __tiles:
#            raise Exception('tile for model already registered')
#        __tiles[tile_class.model.__name__] = tile_class
#
#
#def get_renderer_for_model(model):
#    try:
#        return __tiles[model.__class__.__name__]
#    except KeyError:
#        pass
#    try:
#        return __tiles[model.__name__]
#    except KeyError:
#        pass
#    return None
