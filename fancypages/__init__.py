import os

__version__ = (0, 1, 0, 'alpha', 1)


def get_fancypages_paths(path):
    """ Get absolute paths for *path* relative to the project root """
    return [os.path.join(os.path.dirname(os.path.abspath(__file__)), path)]


def get_apps():
    return (
        'django_extensions',
        # used for image thumbnailing
        'sorl.thumbnail',
        # framework used for the internal API
        'rest_framework',
        # provides a convenience layer around model inheritance
        # that makes lookup of nested models easier. This is used
        # for the content block hierarchy.
        'model_utils',
        # static file compression and collection
        'compressor',
        # migration handling
        'south',
        # package used for twitter block
        'twitter_tag',
        # actual apps provided by fancypages
        'fancypages.assets',
        'fancypages',
    )
