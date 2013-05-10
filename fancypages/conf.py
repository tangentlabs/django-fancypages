from django.conf import settings
from appconf import AppConf


class FancyPagesConf(AppConf):
    DEFAULT_TEMPLATE = "fancypages/pages/page.html"

    class Meta:
        prefix = 'fancypages'
