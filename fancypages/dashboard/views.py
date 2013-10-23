from django import http
from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _

from fancypages.dashboard import forms


FancyPage = get_model('fancypages', 'FancyPage')
ContentBlock = get_model('fancypages', 'ContentBlock')
Category = get_model('catalogue', 'Category')
Container = get_model('fancypages', 'Container')
TabBlock = get_model('fancypages', 'TabBlock')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class PageListView(generic.ListView):
    model = FancyPage
    context_object_name = 'page_list'
    template_name = "fancypages/dashboard/page_list.html"

    def get_queryset(self, queryset=None):
        return self.model.objects.filter(depth=1)


class PageCreateView(generic.CreateView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageCreateForm
    model = FancyPage

    def get_form_kwargs(self):
        kwargs = super(PageCreateView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(PageCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Create new page")
        return ctx

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class PageUpdateView(generic.UpdateView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageForm
    context_object_name = 'page'
    model = FancyPage

    def get_context_data(self, **kwargs):
        ctx = super(PageUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Update page")
        return ctx

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class PageDeleteView(generic.DeleteView):
    model = FancyPage
    template_name = "fancypages/dashboard/page_delete.html"

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class FancypagesMixin(object):

    def get_block_class(self):
        model = None
        for block_class in ContentBlock.itersubclasses():
            if block_class._meta.abstract:
                continue

            if block_class.code == self.kwargs.get('code'):
                model = block_class
                break
        return model

    def get_block_object(self):
        try:
            return self.model.objects.select_subclasses().get(
                id=self.kwargs.get('pk')
            )
        except self.model.DoesNotExist:
            raise http.Http404


class BlockUpdateView(generic.UpdateView, FancypagesMixin):
    model = ContentBlock
    context_object_name = 'block'
    template_name = "fancypages/dashboard/block_update.html"

    def get_object(self, queryset=None):
        return self.get_block_object()

    def get_form_kwargs(self):
        kwargs = super(BlockUpdateView, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_form_class(self):
        model = self.object.__class__
        get_form_class = getattr(model, 'get_form_class')
        if get_form_class and get_form_class():
            return modelform_factory(model, form=get_form_class())

        form_class = getattr(
            forms,
            "%sForm" % model.__name__,
            forms.BlockForm
        )
        return modelform_factory(model, form=form_class)

    def form_invalid(self, form):
        if self.request.is_ajax():
            # FIXME this should actually return a rendered response
            # with the invalid form data init.
            return http.HttpResponseBadRequest()
        return super(BlockUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('fp-dashboard:block-update',
                       args=(self.object.id,))


class BlockDeleteView(generic.DeleteView, FancypagesMixin):
    model = ContentBlock
    context_object_name = 'block'
    template_name = "fancypages/dashboard/block_delete.html"

    def get_object(self, queryset=None):
        return self.get_block_object()

    def delete(self, request, *args, **kwargs):
        response = super(BlockDeleteView, self).delete(request, *args,
                                                       **kwargs)
        blocks = self.object.container.blocks.all().select_subclasses()
        for idx, block in enumerate(blocks):
            block.display_order = idx
            block.save()
        return response

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')
