from sandbox.settings import *

# Setting to use with vagrant and 'mysql' or 'postgres'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
