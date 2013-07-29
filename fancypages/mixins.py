from django import http
from django.conf import settings
from django.db.models import get_model
from django.utils import simplejson as json
from django.utils.encoding import force_unicode
from django.template.defaultfilters import slugify

FancyPage = get_model('fancypages', 'FancyPage')


class FancyPageMixin(object):
    object_attr_name = 'object'

    def get_template_names(self):
        instance = getattr(self, self.object_attr_name)
        if not instance.page_type:
            return [settings.FANCYPAGES_DEFAULT_TEMPLATE]
        return [instance.page_type.template_name]


class FancyHomeMixin(FancyPageMixin):
    HOMEPAGE_NAME = getattr(settings, 'FP_HOMEPAGE_NAME', 'Home')

    def get_object(self):
        slug = slugify(self.HOMEPAGE_NAME)
        try:
            page = FancyPage.objects.get(slug=slug)
        except FancyPage.DoesNotExist:
            page = FancyPage.add_root(
                name=self.HOMEPAGE_NAME,
                slug=slug,
                status=FancyPage.PUBLISHED,
            )
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
