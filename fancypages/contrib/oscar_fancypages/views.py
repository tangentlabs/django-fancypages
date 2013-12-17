from oscar.apps.catalogue.views import ProductCategoryView

from . import mixins


class FancyPageDetailView(mixins.OscarFancyPageMixin, ProductCategoryView):
    pass
