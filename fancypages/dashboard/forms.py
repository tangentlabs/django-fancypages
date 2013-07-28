from copy import copy

from django import forms
from django.db.models import get_model
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

FancyPage = get_model('fancypages', 'FancyPage')
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
            self.fields['visibility_types'].queryset = \
                VisibilityType.objects.all()


class PageForm(PageFormMixin, forms.ModelForm):
    image = forms.ImageField(required=False)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=False)
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
        self.set_field_choices()
        self.update_field_order()

    class Meta:
        model = FancyPage
        fields = ['name', 'keywords', 'page_type', 'status', 'description',
                  'date_visible_start', 'date_visible_end', 'visibility_types']


class PageCreateForm(PageFormMixin, forms.ModelForm):
    image = forms.ImageField(required=False)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=False)
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
            self.parent = FancyPage.objects.get(id=parent_id)
        except FancyPage.DoesNotExist:
            self.parent = None
        self.set_field_choices()
        self.update_field_order()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            FancyPage.objects.get(slug=slugify(name))
        except FancyPage.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                _("A page with this title already exists")
            )
        return name

    def save(self, *args, **kwargs):
        page_kwargs = copy(self.cleaned_data)
        page_kwargs.pop('visibility_types')
        return FancyPage.add_root(**page_kwargs)

    class Meta:
        model = FancyPage
        fields = ['name', 'keywords', 'page_type', 'status', 'description',
                  'date_visible_start', 'date_visible_end', 'visibility_types']


class BlockUpdateSelectForm(forms.Form):
    block_code = forms.ChoiceField(label=_("Edit block:"))

    def __init__(self, container, *args, **kwargs):
        super(BlockUpdateSelectForm, self).__init__(*args, **kwargs)

        block_choices = []
        for block in container.blocks.select_subclasses():
            block_choices.append((block.id, unicode(block)))

        self.fields['block_code'].choices = block_choices


class BlockForm(forms.ModelForm):
    template_name = "fancypages/partials/editor_form_fields.html"

    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput()
        }


class TextBlockForm(BlockForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TitleTextBlockForm(BlockForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TwoColumnLayoutBlockForm(BlockForm):
    left_width = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'data-min': 1,
            # the max value is restricted to '11' in JS but we need the actual
            # max value there so this is the way to pass it through
            'data-max': 12,
        }),
        label=_("Proportion of columns")
    )


class TabBlockForm(BlockForm):

    def __init__(self, *args, **kwargs):
        super(TabBlockForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        if instance:
            for tab in instance.tabs.all():
                field_name = "tab_title_%d" % tab.id
                self.fields[field_name] = forms.CharField()
                self.fields[field_name].initial = tab.title
                self.fields[field_name].label = _("Tab title")

    def save(self):
        instance = super(TabBlockForm, self).save()

        for tab in instance.tabs.all():
            field_name = "tab_title_%d" % tab.id
            tab.title = self.cleaned_data[field_name]
            tab.save()

        return instance
