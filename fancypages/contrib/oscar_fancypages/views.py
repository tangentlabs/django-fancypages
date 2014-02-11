from oscar.core.loading import load_class

from . import mixins


ProductCategoryView = load_class('catalogue.views', 'ProductCategoryView')


class FancyPageDetailView(mixins.OscarFancyPageMixin, ProductCategoryView):
    pass
