########## INSTALLED APPS
FANCYPAGES_REQUIRED_APPS = (
    'rest_framework',
    'model_utils',
    'south',
    'compressor',
    'twitter_tag',
    'sorl.thumbnail',
)
FANCYPAGES_APPS = (
    'fancypages',
    'fancypages.api',
    'fancypages.assets',
    'fancypages.dashboard',
)
########## END INSTALLED APPS

########## COMPRESSOR SETTINGS
# Compressor and pre-compiler settings for django-compressor
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_OUTPUT_DIR = 'cache'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
    'compressor.filters.template.TemplateFilter',
]
########## END COMPRESSOR SETTINGS

########## TWITTER TAG SETTINGS
TWITTER_OAUTH_TOKEN = ''
TWITTER_OAUTH_SECRET = ''
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
########## END TWITTER TAG SETTINGS
