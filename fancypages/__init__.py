import os

__version__ = (0, 0, 1, 'alpha', 1)


def get_fancypages_paths(path):
    return [os.path.join(os.path.dirname(os.path.abspath(__file__)), path)]
