from django.db.models import get_model
from django.template import loader, RequestContext

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication

from fancypages.api import serialisers

Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
Category = get_model('catalogue', 'Category')
Container = get_model('fancypages', 'Container')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class ApiV1View(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({
            'widgets': reverse('fp-api:widget-list', request=request),
        })


class WidgetListView(generics.ListCreateAPIView):
    model = Widget
    serializer_class = serialisers.WidgetSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def pre_save(self, obj):
        if obj.display_order < 0:
            obj.display_order = None
        return obj

    def get_queryset(self):
        return super(WidgetListView, self).get_queryset().select_subclasses()


class WidgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    model = Widget
    serializer_class = serialisers.WidgetSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.model.objects.get_subclass(
            id=self.kwargs.get(self.pk_url_kwarg)
        )


class WidgetMoveView(generics.UpdateAPIView):
    model = Widget
    serializer_class = serialisers.WidgetMoveSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_object(self):
        widget = self.model.objects.get_subclass(
            id=self.kwargs.get(self.pk_url_kwarg)
        )
        widget.prev_container = widget.container
        return widget


class OrderedContainerListView(generics.ListCreateAPIView):
    model = OrderedContainer
    serializer_class = serialisers.OrderedContainerSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)


class PageSelectFormView(APIView):
    form_template_name = "fancypages/dashboard/page_select.html"

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_rendered_form(self):
        tmpl = loader.get_template(self.form_template_name)
        ctx = RequestContext(self.request, {
            'field_id': self.request.GET.get('field_id', 'id_link')
        })
        return tmpl.render(ctx)

    def get(self, request):
        return Response({'rendered_form': self.get_rendered_form()})


class WidgetTypesView(APIView):
    form_template_name = "fancypages/dashboard/widget_select.html"

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request):
        container_id = request.QUERY_PARAMS.get('container')
        if container_id is None:
            return Response({
                    'detail': u'container ID is required for widget list',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            container = Container.objects.get(pk=container_id)
        except Container.DoesNotExist:
            return Response({
                    'detail': u'container ID is invalid',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({
            'groupedWidgets': Widget.get_available_widgets()
        })


class PageMoveView(generics.UpdateAPIView):
    model = Page
    serializer_class = serialisers.PageMoveSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def pre_save(self, obj):
        if obj.new_index <= obj.old_index:
            position = 'left'
        else:
            position = 'right'

        # if the parent ID is '0' the page will be moved to the
        # root level. That means we have to lookup the root node
        # that we use to relate the move to. This is the root node
        # at the position of the new_index. If it is the last node
        # the index will cause a IndexError so we insert the page
        # after the last node.
        if not obj.parent:
            try:
                category = Category.get_root_nodes()[obj.new_index]
            except IndexError:
                category = Category.get_last_root_node()
                position = 'right'

        # in this case the page is moved relative to a parent node.
        # we have to handle the same special case for the last node
        # as above and also have to insert as 'first-child' if no
        # other children are present due to different relative node
        else:
            category = Page.objects.get(id=obj.parent).category
            if not category.numchild:
                position = 'first-child'
            else:
                try:
                    category = category.get_children()[obj.new_index]
                except IndexError:
                    position = 'last-child'

        obj.category.move(category, position)
        return obj
