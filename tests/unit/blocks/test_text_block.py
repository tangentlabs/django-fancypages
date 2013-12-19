import mock

from django.test import TestCase
from django.template import RequestContext

from fancypages.test import factories


class TestTextBlock(TestCase):

    def setUp(self):
        super(TestTextBlock, self).setUp()
        self.user = factories.UserFactory.build()

        self.request_context = RequestContext(mock.MagicMock())
        self.request_context['user'] = self.user

    def test_can_be_rendered_in_template(self):
        block = factories.TextBlockFactory.build(id=6)
        renderer = block.get_renderer_class()(block, self.request_context)
        block_html = renderer.render()

        self.assertIn(
            "block-{0}-{1}".format(block.uuid, block.code), block_html)
        self.assertIn(block.text, block_html)
