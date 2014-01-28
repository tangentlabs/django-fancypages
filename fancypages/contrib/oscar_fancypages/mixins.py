from ... import mixins


class OscarFancyPageMixin(mixins.FancyPageMixin):
    node_attr_name = 'category'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        ctx = super(OscarFancyPageMixin, self).get_context_data(**kwargs)
        ctx['fancypage'] = getattr(self, self.page_attr_name)
        if self.category:
            ctx['object'] = self.category
            for container in self.category.page.containers.all():
                ctx[container.name] = container
        return ctx
