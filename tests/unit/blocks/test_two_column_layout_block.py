import mock

from django.test import TestCase
from django.template import RequestContext

from fancypages.models import Container
from fancypages.models.blocks import TwoColumnLayoutBlock

from fancypages.test import factories


class TestTwoColumnLayoutBlock(TestCase):

    def setUp(self):
        super(TestTwoColumnLayoutBlock, self).setUp()
        self.user = factories.UserFactory.build()

        self.request_context = RequestContext(mock.MagicMock())
        self.request_context['user'] = self.user

    def test_generates_two_empty_containers_when_rendered(self):
        container = Container.objects.create(name='test-container')
        block = TwoColumnLayoutBlock.objects.create(container=container)

        self.assertEquals(block.containers.count(), 0)
        renderer = block.get_renderer_class()(block, self.request_context)
        block_html = renderer.render()

        self.assertEquals(block.containers.count(), 2)
