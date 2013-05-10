from django.db.models import get_model
from django.utils.translation import ugettext as _
from django.forms.models import modelform_factory
from django.template import loader, RequestContext

from rest_framework import serializers

from fancypages.dashboard import forms

Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class RenderFormFieldMixin(object):
    form_template_name = None
    context_object_name = 'object'

    def get_rendered_form(self, obj):
        request = self.context.get('request')
        if not request or 'includeForm' not in request.GET:
            return u''

        form_class = self.get_form_class(obj)
        form_kwargs = self.get_form_kwargs(obj)

        tmpl = loader.get_template(self.form_template_name)
        ctx = RequestContext(
            self.context['request'],
            {
                self.context_object_name: obj,
                'form': form_class(**form_kwargs),
            }
        )
        return tmpl.render(ctx)

    def get_form_kwargs(self, obj):
        return {
            'instance': obj,
        }

    def get_form_class(self, obj):
        # check if the widget has a class-level attribute that
        # defines a specific form class to be used
        form_class = getattr(obj.__class__, 'form_class', None)
        return modelform_factory(obj.__class__, form=form_class)


class WidgetSerializer(RenderFormFieldMixin, serializers.ModelSerializer):
    form_template_name = "fancypages/dashboard/widget_update.html"
    context_object_name = 'widget'

    display_order = serializers.IntegerField(required=False, default=-1)
    code = serializers.CharField(required=True)
    rendered_form = serializers.SerializerMethodField('get_rendered_form')

    def restore_object(self, attrs, instance=None):
        code = attrs.pop('code')

        if instance is None:
            widget_class = self.get_widget_class(code)
            if widget_class:
                self.opts.model = widget_class

        return super(WidgetSerializer, self).restore_object(attrs, instance)

    def get_widget_class(self, code):
        model = None
        for widget_class in Widget.itersubclasses():
            if widget_class._meta.abstract:
                continue

            if widget_class.code == code:
                model = widget_class
                break
        return model

    def get_form_class(self, obj):
        model = self.object.__class__
        form_class = getattr(model, 'form_class')
        if not form_class:
            form_class = getattr(
                forms,
                "%sForm" % model.__name__,
                forms.WidgetForm
            )
        return modelform_factory(model, form=form_class)

    class Meta:
        model = Widget


class WidgetMoveSerializer(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField()
    index = serializers.IntegerField(source='display_order')

    class Meta:
        model = Widget
        read_only_fields = ['display_order']


class OrderedContainerSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField()
    title = serializers.CharField(required=False, default=_("New Tab"))

    def restore_object(self, attrs, instance=None):
        instance = super(OrderedContainerSerializer, self).restore_object(attrs, instance)

        if instance is not None:
            instance.display_order = instance.page_object.tabs.count()

        return instance

    class Meta:
        model = OrderedContainer
        exclude = ['display_order']


class PageMoveSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_page_title')
    is_visible = serializers.SerializerMethodField('get_visibility')

    parent = serializers.IntegerField(required=True)
    new_index = serializers.IntegerField()
    old_index = serializers.IntegerField(required=True)

    def get_page_title(self):
        return self.object.name

    def get_visibility(self):
        return self.object.is_visible

    class Meta:
        model = Page
        fields = ['parent', 'new_index', 'old_index']
        read_only_fields = ['status',]
