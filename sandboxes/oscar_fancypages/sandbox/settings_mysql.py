from sandbox.settings import *

# Setting to use with vagrant and 'mysql' or 'postgres'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'test_app',
        'PASSWORD': 'test_app',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
