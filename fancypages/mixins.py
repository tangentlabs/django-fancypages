from django import http
from django.conf import settings
from django.utils import simplejson as json
from django.utils.encoding import force_unicode
from django.template.defaultfilters import slugify

from .models import get_page_model
from .defaults import FP_HOMEPAGE_NAME

FancyPage = get_page_model()


class FancyPageMixin(object):
    object_attr_name = 'object'

    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug'

    page_attr_name = 'page'
    node_attr_name = 'node'

    def get_object(self):
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
        slug = slugify(self.HOMEPAGE_NAME)
        try:
            page = FancyPage.objects.get(node__slug=slug)
        except FancyPage.DoesNotExist:
            page = FancyPage.add_root(
                node__name=self.HOMEPAGE_NAME, node__slug=slug,
                status=FancyPage.PUBLISHED)
        return page


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
