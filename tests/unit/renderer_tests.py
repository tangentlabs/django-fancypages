from django.test import TestCase

from fancypages import loaders
from fancypages.models import TextTile
from fancypages.serializers import HtmlSerializer


class TestAStaticTile(TestCase):

    def test_can_be_rendered_to_html(self):
        tile = TextTile.objects.create(text="Test text")
        renderer_class = loaders.get_renderer_for_model(tile)

        renderer = renderer_class(tile)
        renderer.serializer = HtmlSerializer

        print renderer.render()
