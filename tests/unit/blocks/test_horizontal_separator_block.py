import mock

from django.test import TestCase
from django.template import RequestContext

from fancypages.test import factories


class TestHorizontalSeparatorBlock(TestCase):

    def setUp(self):
        super(TestHorizontalSeparatorBlock, self).setUp()
        self.user = factories.UserFactory.build()

        self.request_context = RequestContext(mock.MagicMock())
        self.request_context['user'] = self.user

    def test_can_be_rendered_in_template(self):
        block = factories.HorizontalSeparatorBlockFactory.build(id=6)
        renderer = block.get_renderer_class()(block, self.request_context)
        block_html = renderer.render()
        self.assertIn('<hr />', block_html)
