from django.http import Http404
from django.conf import settings
from django.db.models import get_model
from django.template.defaultfilters import slugify

from ... import mixins
from ...models import get_page_model

FancyPage = get_page_model()
Container = get_model('fancypages', 'Container')


class OscarFancyPageMixin(object):
    DEFAULT_TEMPLATE = getattr(settings, 'FP_DEFAULT_TEMPLATE')

    def get_template_names(self):
        if not self.category.page_type:
            return [self.DEFAULT_TEMPLATE]
        return [self.category.page_type.template_name]

    def get_object(self):
        try:
            return FancyPage.objects.select_related('page__containers').get(
                node__slug=self.kwargs.get('slug'))
        except (FancyPage.DoesNotExist, FancyPage.MultipleObjectsReturned):
            raise Http404

    def get_context_data(self, **kwargs):
        ctx = super(OscarFancyPageMixin, self).get_context_data(**kwargs)
        if self.category:
            ctx['object'] = ctx[self.context_object_name] = self.category
            for container in self.category.page.containers.all():
                ctx[container.name] = container
        return ctx


class OscarFancyHomeMixin(mixins.FancyHomeMixin, OscarFancyPageMixin):
    object_attr_name = 'category'

    def get(self, request, *args, **kwargs):
        self.kwargs.setdefault('category_slug', slugify(self.HOMEPAGE_NAME))
        self.category = self.get_object()
        response = super(OscarFancyHomeMixin, self).get(
            request, *args, **kwargs)
        if request.user.is_staff:
            return response

        if not self.category.is_visible:
            raise Http404

        return response
