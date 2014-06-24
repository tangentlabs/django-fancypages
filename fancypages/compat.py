# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

_user_model = None


def get_user_model():
    """
    Get the Django user model class in a backwards compatible way to previous
    Django version that don't provide this functionality. The result is cached
    after the first call.

    Returns the user model class.
    """
    global _user_model

    if not _user_model:
        # we have to import the user model here because we can't be sure
        # that the app providing the user model is fully loaded.
        try:
            from django.contrib.auth import get_user_model
        except ImportError:
            from django.contrib.auth.models import User
        else:
            User = get_user_model()
        _user_model = User
    return _user_model


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

try:
    AUTH_USER_MODEL_NAME = AUTH_USER_MODEL.split('.')[1]
except IndexError:
    raise ImproperlyConfigured(
        "invalid user model '{}' specified has to be in the format "
        "'app_label.model_name'.".format(AUTH_USER_MODEL))
