try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


def get_user_model():
    return User


AUTH_USER_MODEL = '{}.{}'.format(User._meta.app_label, User._meta.object_name)
AUTH_USER_MODEL_NAME = User._meta.object_name
