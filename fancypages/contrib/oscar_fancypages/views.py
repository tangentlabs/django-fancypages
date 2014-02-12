from oscar.core.loading import get_class

from . import mixins


ProductCategoryView = get_class('catalogue.views', 'ProductCategoryView')


class FancyPageDetailView(mixins.OscarFancyPageMixin, ProductCategoryView):
    pass
