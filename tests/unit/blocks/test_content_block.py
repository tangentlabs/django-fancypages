from django.test import TestCase
from django.db.models import get_model

from fancypages.test import factories

ContentBlock = get_model('fancypages', 'ContentBlock')


class TestContentBlock(TestCase):

    def test_returns_block_subclasses_in_display_order(self):
        container = factories.ContainerFactory()
        bottom_block = factories.TextBlockFactory(
            container=container,
            display_order=2
        )
        top_block = factories.TextBlockFactory(
            container=container,
            display_order=0
        )
        middle_block = factories.TextBlockFactory(
            container=container,
            display_order=1
        )
        self.assertSequenceEqual(
            [b.id for b in ContentBlock.objects.select_subclasses()],
            [top_block.id, middle_block.id, bottom_block.id]
        )
