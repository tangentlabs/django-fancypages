# FANCYPAGES SETTINGS
FP_HOMEPAGE_NAME = 'Home'
FP_DEFAULT_TEMPLATE = 'fancypages/pages/page.html'
FP_DEFAULT_PAGE_STATUS = 'draft'
FP_PAGE_MODEL = 'fancypages.FancyPage'
FP_NODE_MODEL = 'fancypages.PageNode'
FP_PAGE_DETAIL_VIEW = 'fancypages.views.FancyPageDetailView'
FP_PAGE_URLPATTERN = r'^(?P<slug>[\w-]+(/[\w-]+)*)/$'

# TWITTER TAG SETTINGS
TWITTER_OAUTH_TOKEN = ''
TWITTER_OAUTH_SECRET = ''
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

FANCYPAGES_SETTINGS = dict([(k, v) for k, v in locals().items()])
