from sandbox.settings import *

# Setting to use with vagrant and 'mysql' or 'postgres'
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_db',
        'USER': 'test_app',
        'PASSWORD': 'test_app',
        'HOST': 'localhost',
        #'PORT': 8336, # mysql
	'PORT': 5432, # postgres
    }
}
