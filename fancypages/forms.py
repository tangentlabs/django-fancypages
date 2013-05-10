from django import forms
from django.db.models import get_model
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

Page = get_model('fancypages', 'Page')
Category = get_model('catalogue', 'Category')
PageType = get_model('fancypages', 'PageType')
VisibilityType = get_model('fancypages', 'VisibilityType')


DATE_FORMAT = '%d-%m-%Y'


class PageFormMixin(object):

    def update_field_order(self):
        # we need to specify the key order here because 'description' and
        # 'image' are non-model fields that cause an error when added
        # to the metaclass field attribute below
        self.fields.keyOrder = [
            'name',
            'description',
            'image',
            'keywords',
            'page_type',
            'status',
            'date_visible_start',
            'date_visible_end',
            'visibility_types'
        ]

    def set_field_choices(self):
        if 'page_type' in self.fields:
            self.fields['page_type'].queryset = PageType.objects.all()
        if 'visibility_types' in self.fields:
            self.fields['visibility_types'].queryset = VisibilityType.objects.all()

    def save_category_data(self, category):
        category.name = self.cleaned_data['name']
        category.description = self.cleaned_data['description']
        category.image = self.cleaned_data['image']
        category.save()


class PageForm(PageFormMixin, forms.ModelForm):
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=True)
    date_visible_start = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    date_visible_end = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    visibility_types = forms.ModelMultipleChoiceField(
        VisibilityType.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance is not None:
            self.fields['description'].value = instance.category.description
            self.fields['image'].value = instance.category.image

        self.set_field_choices()
        self.update_field_order()

    def save(self, commit=True):
        self.save_category_data(self.instance.category)
        return super(PageForm, self).save(commit=True)

    class Meta:
        model = Page
        fields = ['name', 'keywords', 'page_type', 'status',
                  'date_visible_start', 'date_visible_end', 'visibility_types']


class PageCreateForm(PageFormMixin, forms.ModelForm):
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=True)
    date_visible_start = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    date_visible_end = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    visibility_types = forms.ModelMultipleChoiceField(
        VisibilityType.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        parent_id = kwargs.pop('parent_pk', None)
        super(PageCreateForm, self).__init__(*args, **kwargs)
        try:
            self.parent = Category.objects.get(id=parent_id)
        except Category.DoesNotExist:
            self.parent = None
        self.set_field_choices()
        self.update_field_order()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Page.objects.get(category__slug=slugify(name))
        except Page.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                _("A page with this title already exists")
            )
        return name

    def save(self, commit=True):
        page_name = self.cleaned_data['name']
        if self.parent:
            category = self.parent.add_child(name=page_name)
        else:
            category = Category.add_root(name=page_name)
        self.save_category_data(category)

        instance = super(PageCreateForm, self).save(commit=False)
        # this is a bit of a hack but we cannot create a new
        # instance here because it has already been created using
        # a post_save signal on the category.
        instance.id = category.page.id
        instance.category = category
        instance.save()
        return instance

    class Meta:
        model = Page
        fields = ['name', 'keywords', 'page_type', 'status',
                  'date_visible_start', 'date_visible_end', 'visibility_types']


class WidgetUpdateSelectForm(forms.Form):
    widget_code = forms.ChoiceField(label=_("Edit widget:"))

    def __init__(self, container, *args, **kwargs):
        super(WidgetUpdateSelectForm, self).__init__(*args, **kwargs)

        widget_choices = []
        for widget in container.widgets.select_subclasses():
            widget_choices.append((widget.id, unicode(widget)))

        self.fields['widget_code'].choices = widget_choices


class WidgetForm(forms.ModelForm):
    template_name = "fancypages/partials/editor_form_fields.html"

    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput()
        }


class TextWidgetForm(WidgetForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TitleTextWidgetForm(WidgetForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TwoColumnLayoutWidgetForm(WidgetForm):
    left_width = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'data-min': 1,
            # the max value is restricted to '11' in JS but we need the actual
            # max value there so this is the way to pass it through
            'data-max': 12,
        }),
        label=_("Proportion of columns")
    )


class TabWidgetForm(WidgetForm):

    def __init__(self, *args, **kwargs):
        super(TabWidgetForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        if instance:
            for tab in instance.tabs.all():
                field_name = "tab_title_%d" % tab.id
                self.fields[field_name] = forms.CharField()
                self.fields[field_name].initial = tab.title
                self.fields[field_name].label = _("Tab title")

    def save(self):
        instance = super(TabWidgetForm, self).save()

        for tab in instance.tabs.all():
            field_name = "tab_title_%d" % tab.id
            tab.title = self.cleaned_data[field_name]
            tab.save()

        return instance
