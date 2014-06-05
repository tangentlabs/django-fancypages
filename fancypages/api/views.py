from django.db.models import get_model
from django.template import loader, RequestContext

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication

from . import serialisers
from ..library import get_grouped_content_blocks
from ..utils import get_page_model, get_node_model

FancyPage = get_page_model()
PageNode = get_node_model()
Container = get_model('fancypages', 'Container')
ContentBlock = get_model('fancypages', 'ContentBlock')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class BlockAPIMixin(object):
    model = ContentBlock
    lookup_field = 'uuid'
    serializer_class = serialisers.BlockSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)


class BlockListView(BlockAPIMixin, generics.ListCreateAPIView):

    def pre_save(self, obj):
        if obj.display_order < 0:
            obj.display_order = None
        return obj

    def get_queryset(self):
        return super(BlockListView, self).get_queryset().select_subclasses()


class BlockDetailView(BlockAPIMixin, generics.RetrieveUpdateDestroyAPIView):

    def get_object(self):
        return self.model.objects.get_subclass(
            uuid=self.kwargs.get(self.lookup_field))

    def post_delete(self, obj):
        """
        After deleting a block, the display order of all blocks in the same
        container is wrong (unless we removed the last block). To fix it, this
        hook iterates over all blocks in the same container and and sets the
        new display_order in each block.
        """
        blocks = obj.container.blocks.select_subclasses()
        for idx, block in enumerate(blocks):
            block.display_order = idx
            block.save()


class BlockNewView(generics.CreateAPIView):
    model = ContentBlock
    serializer_class = serialisers.BlockCodeSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)


class BlockFormView(BlockAPIMixin, generics.RetrieveAPIView):
    serializer_class = serialisers.BlockFormSerializer

    def get_object(self):
        return self.model.objects.get_subclass(
            uuid=self.kwargs.get(self.lookup_field))


class BlockMoveView(BlockAPIMixin, generics.UpdateAPIView):
    serializer_class = serialisers.BlockMoveSerializer

    def get_object(self):
        block = self.model.objects.get_subclass(
            uuid=self.kwargs.get(self.lookup_field))
        block.prev_container = block.container
        return block


class OrderedContainerListView(generics.ListCreateAPIView):
    model = OrderedContainer
    serializer_class = serialisers.OrderedContainerSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)


class OrderedContainerDestroyView(generics.DestroyAPIView):
    model = OrderedContainer
    lookup_field = 'uuid'

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
        container_uuid = request.QUERY_PARAMS.get('container')
        if container_uuid is None:
            return Response(
                {'detail': u'container ID is required for block list'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Container.objects.get(uuid=container_uuid)
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
    lookup_field = 'uuid'
    serializer_class = serialisers.PageMoveSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)


class PageList(generics.ListAPIView):
    model = PageNode
    lookup_field = 'uuid'
    serializer_class = serialisers.PageNodeSerializer

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        qs = super(PageList, self).get_queryset().filter(depth=1)
        return qs
