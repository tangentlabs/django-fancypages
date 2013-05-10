from django import http
from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _

from fancypages.dashboard import forms


Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
Category = get_model('catalogue', 'Category')
Container = get_model('fancypages', 'Container')
TabWidget = get_model('fancypages', 'TabWidget')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class PageListView(generic.ListView):
    model = Page
    context_object_name = 'page_list'
    template_name = "fancypages/dashboard/page_list.html"

    def get_queryset(self, queryset=None):
        return self.model.objects.filter(category__depth=1)


class PageCreateView(generic.CreateView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageCreateForm
    model = Page

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
    model = Page

    def get_initial(self):
        initial = super(PageUpdateView, self).get_initial()
        try:
            category = self.object.category
        except Category.DoesNotExist:
            return initial
        # add exposed category attributes to initial values
        # to make sure that they are displayed in the edit form
        initial['name'] = category.name
        initial['description'] = category.description
        initial['image'] = category.image
        return initial

    def get_context_data(self, **kwargs):
        ctx = super(PageUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Update page")
        return ctx

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class PageDeleteView(generic.DeleteView):
    model = Page
    template_name = "fancypages/dashboard/page_delete.html"

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class FancypagesMixin(object):

    def get_widget_class(self):
        model = None
        for widget_class in Widget.itersubclasses():
            if widget_class._meta.abstract:
                continue

            if widget_class.code == self.kwargs.get('code'):
                model = widget_class
                break
        return model

    def get_widget_object(self):
        try:
            return self.model.objects.select_subclasses().get(
                id=self.kwargs.get('pk')
            )
        except self.model.DoesNotExist:
            raise http.Http404


class WidgetUpdateView(generic.UpdateView, FancypagesMixin):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_update.html"

    def get_object(self, queryset=None):
        return self.get_widget_object()

    def get_form_kwargs(self):
        kwargs = super(WidgetUpdateView, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_form_class(self):
        model = self.object.__class__
        form_class = getattr(model, 'form_class')
        if not form_class:
            form_class = getattr(
                forms,
                "%sForm" % model.__name__,
                forms.WidgetForm
            )
        return modelform_factory(model, form=form_class)

    def form_invalid(self, form):
        if self.request.is_ajax():
            # FIXME this should actually return a rendered response
            # with the invalid form data init.
            return http.HttpResponseBadRequest()
        return super(WidgetUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('fp-dashboard:widget-update',
                       args=(self.object.id,))


class WidgetDeleteView(generic.DeleteView, FancypagesMixin):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_delete.html"

    def get_object(self, queryset=None):
        return self.get_widget_object()

    def delete(self, request, *args, **kwargs):
        response = super(WidgetDeleteView, self).delete(request, *args, **kwargs)
        for idx, widget in enumerate(self.object.container.widgets.all().select_subclasses()):
            widget.display_order = idx
            widget.save()
        return response

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')
