from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse
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
