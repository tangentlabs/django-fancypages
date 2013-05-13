from django import http
from django.utils import simplejson as json
from django.utils.encoding import force_unicode


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
        response['Content-Disposition'] = 'inline; filename=%s' % self.json_filename
        return response

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)
