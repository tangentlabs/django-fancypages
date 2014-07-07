from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from ..utils import unicode_slugify as slugify
from ..utils import get_page_model, get_node_model

PageNode = get_node_model()
FancyPage = get_page_model()
PageType = get_model('fancypages', 'PageType')
PageGroup = get_model('fancypages', 'PageGroup')

DATE_FORMAT = '%d-%m-%Y'


class PageNodeForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        label=_("Groups"), queryset=PageGroup.objects.none(),
        widget=forms.CheckboxSelectMultiple(), required=False)

    class Meta:
        model = FancyPage
        exclude = ['uuid', 'node']

    def __init__(self, *args, **kwargs):
        self.parent_pk = kwargs.pop('parent_pk', None)
        super(PageNodeForm, self).__init__(*args, **kwargs)

        self.fields['groups'].queryset = PageGroup.objects.all()

        # we just need to store these for later to set the key order
        page_field_names = self.fields.keys()

        self.node_field_names = []
        for field in PageNode._meta.fields:
            if field.editable and \
               field.name not in ['id', 'depth', 'numchild', 'path', 'slug']:
                self.node_field_names.append(field.name)

        additional_fields = forms.fields_for_model(
            PageNode, fields=self.node_field_names)
        self.fields.update(additional_fields)

        # if we have a node instance, initialise the page-related fields
        # with the appropriate values
        instance = kwargs.get('instance')
        if instance:
            for field_name in self.node_field_names:
                self.fields[field_name].initial = getattr(
                    instance.node, field_name)

        # update the field order for the page and node fields
        self.fields.keyOrder = self.node_field_names + page_field_names

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.instance.id is not None:
            return name
        try:
            FancyPage.objects.get(node__slug=slugify(name))
        except FancyPage.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                _("A page with this title already exists"))
        return name

    def save(self, *args, **kwargs):
        page_data = {}
        node_data = {}
        for fname, fvalue in self.cleaned_data.iteritems():
            if fname in self.node_field_names:
                node_data[fname] = fvalue
            else:
                page_data[fname] = fvalue

        if not self.instance.id:
            try:
                parent = FancyPage.objects.get(pk=self.parent_pk)
            except FancyPage.DoesNotExist:
                parent = None

            if parent:
                self.instance.node = parent.node.add_child(**node_data)
            else:
                self.instance.node = PageNode.add_root(**node_data)
        else:
            for key, value in node_data.iteritems():
                setattr(self.instance.node, key, value)
            self.instance.node.save()

        return super(PageNodeForm, self).save(*args, **kwargs)


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
        widgets = {'display_order': forms.HiddenInput()}


class TextBlockForm(BlockForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10})}


class TitleTextBlockForm(BlockForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10})}


class TwoColumnLayoutBlockForm(BlockForm):
    left_width = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'min': 1,
            # the max value is restricted to '11' in JS but we need the actual
            # max value there so this is the way to pass it through
            'max': 12,
            'type': 'range',
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


class FormBlockForm(BlockForm):
    form_selection = forms.ChoiceField(label=_("form selection"))

    def __init__(self, *args, **kwargs):
        super(FormBlockForm, self).__init__(*args, **kwargs)
        from fancypages.helpers import BlockFormSettings
        settings = BlockFormSettings()
        self.fields['form_selection'].choices = tuple(settings.as_choices())
