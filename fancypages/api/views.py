from django.db.models import get_model
from django.template import loader, RequestContext

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication

from . import renderers
from . import serialisers
from ..library import get_grouped_content_blocks

FancyPage = get_model('fancypages', 'FancyPage')
Container = get_model('fancypages', 'Container')
ContentBlock = get_model('fancypages', 'ContentBlock')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class BlockListView(generics.ListCreateAPIView):
    model = ContentBlock
    serializer_class = serialisers.BlockSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def pre_save(self, obj):
        if obj.display_order < 0:
            obj.display_order = None
        return obj

    def get_queryset(self):
        return super(BlockListView, self).get_queryset().select_subclasses()


class BlockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    model = ContentBlock
    serializer_class = serialisers.BlockSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.model.objects.get_subclass(
            id=self.kwargs.get(self.pk_url_kwarg))


class BlockFormView(generics.RetrieveAPIView):
    model = ContentBlock
    serializer_class = serialisers.BlockSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    renderer_classes = (renderers.BlockFormRenderer,)

    def get_object(self):
        return self.model.objects.get_subclass(
            id=self.kwargs.get(self.pk_url_kwarg))


class BlockMoveView(generics.UpdateAPIView):
    model = ContentBlock
    serializer_class = serialisers.BlockMoveSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_object(self):
        block = self.model.objects.get_subclass(
            id=self.kwargs.get(self.pk_url_kwarg)
        )
        block.prev_container = block.container
        return block


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


class BlockTypesView(APIView):
    form_template_name = "fancypages/dashboard/block_select.html"

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request):
        container_id = request.QUERY_PARAMS.get('container')
        if container_id is None:
            return Response(
                {'detail': u'container ID is required for block list'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Container.objects.get(pk=container_id)
        except Container.DoesNotExist:
            return Response(
                {'detail': u'container ID is invalid'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({
            'groupedBlocks': get_grouped_content_blocks(),
        })


class PageMoveView(generics.UpdateAPIView):
    model = FancyPage
    serializer_class = serialisers.PageMoveSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
