from __future__ import absolute_import

from django.http import Http404

from oscar.apps.catalogue.views import ProductCategoryView

from . import mixins
from ...models import get_page_model

FancyPage = get_page_model()


class FancyPageDetailView(mixins.OscarFancyPageMixin, ProductCategoryView):
    context_object_name = 'fancypage'

    def get_context_data(self, **kwargs):
        context = super(FancyPageDetailView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.category
        context['object'] = self.category
        context['summary'] = self.category.name
        return context

    def get_categories(self):
        """
        Return a list of the current page/category and it's ancestors
        """
        categories = [self.category]
        categories.extend(list(self.category.get_descendants()))
        return categories

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            self.category = FancyPage.objects.get(node__slug=slug)
        except FancyPage.DoesNotExist:
            raise Http404()
        response = super(FancyPageDetailView, self).get(
            request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.category.is_visible:
            raise Http404

        return response


class FancyHomeView(mixins.OscarFancyHomeMixin, ProductCategoryView):
    model = FancyPage
    context_object_name = 'fancypage'
