# -*- coding: utf-8 -*-
import json

from django import http
from django.conf import settings
from django.utils.encoding import force_unicode
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from .utils import get_page_model
from .defaults import FP_HOMEPAGE_NAME
from .utils import unicode_slugify as slugify


class FancyPageMixin(object):
    object_attr_name = 'object'

    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug'

    page_attr_name = 'page'
    node_attr_name = 'node'

    def get_object(self):
        FancyPage = get_page_model()
        try:
            page = FancyPage.objects.select_related('node__containers').get(
                node__slug=self.kwargs.get(self.slug_url_kwarg))
        except FancyPage.DoesNotExist:
            raise http.Http404()
        return page

    def get_template_names(self):
        page = getattr(self, self.page_attr_name)
        if not page.page_type:
            return [settings.FP_DEFAULT_TEMPLATE]
        return [page.page_type.template_name]

    def get(self, request, *args, **kwargs):
        page = self.get_object()

        if not request.user.is_staff:
            if not page.is_visible:
                raise http.Http404()

        setattr(self, self.page_attr_name, page)
        setattr(self, self.node_attr_name, page.node)

        return super(FancyPageMixin, self).get(request, *args, **kwargs)


class FancyHomeMixin(FancyPageMixin):
    HOMEPAGE_NAME = getattr(settings, 'FP_HOMEPAGE_NAME', FP_HOMEPAGE_NAME)

    def get_object(self):
        FancyPage = get_page_model()
        slug = slugify(self.HOMEPAGE_NAME)
        try:
            page = FancyPage.objects.get(node__slug=slug)
        except FancyPage.DoesNotExist:
            page = FancyPage.add_root(
                node__name=self.HOMEPAGE_NAME, node__slug=slug,
                status=FancyPage.PUBLISHED)
        return page


class TemplateNamesModelMixin(object):
    """
    Mixin that provides a generalised way of generating template names for a
    a Django model. It uses relies on at least one of two class attributes:
    ``template_name`` and ``default_template_names`` to generate a list of
    templates to look for according to Django's rules for template lookup.

    The ``template_name`` attribute specifies a specific template to be used
    when rendering this model. If this attribute is not ``None`` it takes
    precedence over all other template names and therefore will appear at the
    top of the templates. The ``default_template_names`` is a list of template
    names that provides default behaviour and a fallback in case no template
    name is given or it can't be found by the template engine. Specifying both
    a template name and a list of default templates will result in a list of
    template names similar to this:

    .. doctest::

        >>> from django.db import models
        >>> from fancypages.mixins import TemplateNamesModelMixin
        >>>
        >>> class Container(TemplateNamesModelMixin, models.Model):
        ...     template_name = 'container.html'
        ...     default_template_names = ['default_container.html']
        ...
        ...     class Meta: app_label = 'fakeapp'
        >>>
        >>>
        >>> c = Container()
        >>> c.get_template_names()
        ['container.html', 'default_container.html']

    Each template name provided in ``template_name`` or
    ``default_template_names`` is also run through standard Python string
    formatting providing the model name as provide in
    ``self._meta.module_name`` which allows parametrized template names.
    Additional keyword arguments can be passed into ``get_template_names`` to
    provide additional formatting keywords. Here's an example:

    .. doctest::

        >>> class Pony(TemplateNamesModelMixin, models.Model):
        ...     template_name = 'container_{module_name}_{magic}.html'
        ...
        ...     class Meta: app_label = 'fakeapp'
        >>>
        >>> c = Pony()
        >>> c.get_template_names(magic='rainbow')
        ['container_pony_rainbow.html']

    In addition to the above, language-specific template names are added
    if the model has a ``language_code`` attribute specified. This allows
    different templates for different languages to customise the appearance
    of the rendered data based on the language. This makes sense for langugages
    such as Persian where the reading direction is from left to right.
    Language-specific templates have the corresponding language code added as a
    suffix to the filename just before the file extension. In cases such as
    English where the language is split up into different regions such as
    British (en-gb) and American English (en-us) a generic template for 'en' is
    added as well. For a British language code this will be the list of
    templates::

        >>> class Pony(TemplateNamesModelMixin, models.Model):
        ...     template_name = '{module_name}.html'
        ...     language_code = models.CharField(max_length=6)
        ...
        ...     class Meta: app_label = 'fakeapp'
        >>>
        >>> c = Pony(language_code='en-gb')
        >>> c.get_template_names()
        ['pony_en-gb.html', 'pony_en.html', 'pony.html']


    """
    template_name = None
    default_template_names = []

    def get_template_names(self, **kwargs):
        """
        Get a list of template names in order of precedence as used by the
        Django template engine. Keyword argument passed in are used during
        string formatting of the template names. This fails silently if a
        argument is specified in a template name but is not present in
        ``kwargs``.

        :rtype list: A list of template names (unicode).
        """
        if not self.template_name and not self.default_template_names:
            raise ImproperlyConfigured(
                _("No template name and default templates specified."))
        default_names = list(self.default_template_names)

        template_kwargs = {'module_name': self._meta.module_name}
        template_kwargs.update(kwargs)

        if self.template_name:
            default_names = [self.template_name] + default_names

        language_code = getattr(self, 'language_code', None)

        try:
            parent_code, __ = language_code.split('-')
        except (AttributeError, ValueError):
            parent_code = None

        template_names = []
        for tmpl_name in default_names:
            try:
                tmpl_name = tmpl_name.format(**template_kwargs)
            except KeyError:
                pass

            basename, ext = tmpl_name.rsplit('.', 1)

            if language_code:
                template_names.append(
                    "{}_{}.{}".format(basename, language_code, ext))

            # add a fallback for the parent language if it is available
            # e.g. for 'en-gb' we want 'en' to be a fallback template
            if parent_code:
                template_names.append(
                    "{}_{}.{}".format(basename, parent_code, ext))

            template_names.append(tmpl_name)

        return template_names


class JSONResponseMixin(object):
    json_filename = 'response.json'

    def get_content_type(self):
        http_accept = self.request.META.get('HTTP_ACCEPT', [])
        if "application/json" in http_accept:
            return "application/json"
        else:
            return "text/plain"

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        if 'success' not in context:
            context['success'] = True
        return self.get_json_response(self.convert_context_to_json(context))

    def render_to_error_response(self, reason, context=None):
        if context is None:
            context = {}
        context['success'] = False
        context['reason'] = force_unicode(reason)
        return self.render_to_response(context)

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        response = http.HttpResponse(
            content,
            content_type=self.get_content_type(),
            **httpresponse_kwargs
        )
        response['Content-Disposition'] = 'inline; filename={0}'.format(
            self.json_filename
        )
        return response

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)
