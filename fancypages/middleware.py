import re

from django.template import RequestContext
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string

BODY_STARTTAG = re.compile(r'(?P<body_tag><body[^>]+>)')


def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive
    Code borrowed from:
    http://forums.devshed.com/python-programming-11/
            case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else:  # no results so return the original string
        return string


class EditorMiddleware(object):
    body_tag = '</body>'
    head_tag = '</head>'
    body_template_name = 'fancypages/editor/body.html'
    head_template_name = 'fancypages/editor/head.html'

    def process_request(self, request):
        edit_mode = False
        if request.user.is_authenticated() and request.user.is_staff:
            edit_mode = True
        request.fancypages_edit_mode = edit_mode

    def process_response(self, request, response):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated():
            return response
        if not user.is_staff:
            return response

        if 'editable-container' not in response.content:
            return response

        editor_head = render_to_string(
            self.head_template_name,
            RequestContext(request)
        )
        response.content = replace_insensitive(
            smart_unicode(response.content),
            self.head_tag,
            smart_unicode(editor_head) + self.head_tag,
        )

        response.content = BODY_STARTTAG.sub(
            r'\g<body_tag><div class="editable-page-wrapper">',
            response.content
        )

        editor_body = render_to_string(
            self.body_template_name,
            RequestContext(request)
        )
        response.content = replace_insensitive(
            smart_unicode(response.content),
            self.body_tag,
            "%s%s%s" % ("</div>", smart_unicode(editor_body), self.body_tag),
        )

        if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)
        return response
