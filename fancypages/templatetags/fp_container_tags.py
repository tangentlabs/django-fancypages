from django import template
from django.db.models import get_model
from django.template.base import token_kwargs


register = template.Library()


def parse_arguments(parser, token, params=None):
    """
    Parse positional arguments and keyword arguments into a dictionary for the
    known arguments given in *params* in the given order. If the number of
    arguments in *token* is greater than the known number of arguments, a
    ``TemplateSyntaxError`` is raised. The same is true if no tokens are
    provided.

    :param parser: Parser as passed into the template tag.
    :param token: Token object as passed into the template tag.
    :param params: List of expected arguments in the order in which they appear
        when not using keyword arguments. Default to ['container_name',
        'object_name', 'language'].
    :rtype dict: containing the parsed content for the arguments above.
    """
    bits = token.split_contents()[1:]
    if not params:
        params = ['container_name', 'object_name', 'language']

    if len(bits) > len(params):
        raise template.TemplateSyntaxError(
            "{} arguments specified but only {} are allowed".format(
                len(bits), len(params)))

    if not bits:
        raise template.TemplateSyntaxError(
            "%r tag requires container name as first argument and "
            " optionally object" % token.contents.split()[0])

    parsed_kwargs = {}
    for idx, bit in enumerate(bits):
        kwarg = token_kwargs([bit], parser)
        if kwarg:
            param, value = list(kwarg.iteritems())[0]
            parsed_kwargs[param] = value.var
        else:
            parsed_kwargs[params[idx]] = bit
    return parsed_kwargs


class ContainerNodeMixin(object):

    def get_object(self, context):
        if not self.object_name:
            return None
        try:
            return self.object_name.resolve(context)
        except template.VariableDoesNotExist:
            pass
        return None

    def get_container(self, context):
        Container = get_model('fancypages', 'Container')
        # check first if the container name refers to a
        # variable in the context and use it a container
        try:
            return self.container_name.resolve(context)
        except template.VariableDoesNotExist:
            pass
        # container variable is not in the context. we have to look
        # up the container from the variable name and - if the object
        # is not None - the object the container is attached to.
        try:
            return Container.get_container_by_name(
                name=self.container_name.var, obj=self.object)
        except KeyError:
            pass
        return None

    def render(self, context):
        """
        Render the container provided by the ``container_name`` variable
        name in this node. If a node with this name exists in the
        context, the context variable will be used as container. Otherwise,
        we try to retrieve a container based on the variable name using
        the ``object`` variable in the context.
        """
        self.object = self.get_object(context)
        self.container = self.get_container(context)

        if not self.container:
            return u''

        from fancypages.renderers import ContainerRenderer
        renderer = ContainerRenderer(self.container, context)
        return renderer.render()


class FancyContainerNode(ContainerNodeMixin, template.Node):

    def __init__(self, container_name, language=None):
        self.container_name = template.Variable(container_name)
        self.object_name = None


class FancyObjectContainerNode(ContainerNodeMixin, template.Node):

    def __init__(self, container_name, object_name=None, language=None):
        self.container_name = template.Variable(container_name)
        self.object_name = template.Variable(object_name or 'object')


@register.tag
def fp_container(parser, token):
    params = ['container_name', 'language']
    return FancyContainerNode(**parse_arguments(parser, token, params))


@register.tag
def fp_object_container(parser, token):
    """
    Template tag specifying a fancypages container to be rendered in the
    template at the given location. It takes up to three arguments. The first
    argument is the name of the container which is mandatory. The object that
    this tag is attached to is the second argument and is optional. If it is
    not specified, the 'object' variable in the current context is used. The
    third argument is an optional language code that specify the language that
    should be used for the container. Without a language code specified, the
    current language is retrieved using Django's internationalisation helpers.

    Valid template tags are::

        {% fp_object_container container-name %}

    and with a specific object::

        {% fp_object_container container-name my_object %}

    and with a language code::

        {% fp_object_container container-name my_object "de-de" %}
        {% fp_object_container container-name object_name=my_object language="de-de" %}
    """
    return FancyObjectContainerNode(**parse_arguments(parser, token))


@register.tag
def fp_block_container(parser, token):
    """
    Template tag for convenience to use within templates for e.g. layout blocks
    where the container is assigned to the widget rather then the object in the
    context. The same could be achieved using::

        {% fp_object_container some-name fp_block %}
    """
    parsed_kwargs = parse_arguments(parser, token)
    parsed_kwargs['object_name'] = 'fp_block'
    return FancyObjectContainerNode(**parsed_kwargs)
