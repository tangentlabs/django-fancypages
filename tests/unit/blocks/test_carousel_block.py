from django.db.models import get_model
from fancypages.test.testcases import BlockTestCase

CarouselBlock = get_model('fancypages', 'CarouselBlock')


class TestCarouselBlock(BlockTestCase):

    def test_has_10_image_attributes(self):
        carousel = CarouselBlock()
        for idx in range(1, 11):
            self.assertTrue(hasattr(carousel, carousel.image_field_name % idx))

    def test_has_10_link_attributes(self):
        carousel = CarouselBlock()
        for idx in range(1, 11):
            self.assertTrue(hasattr(carousel, carousel.link_field_name % idx))

    def test_can_be_rendered_in_template(self):
        html = self.get_rendered_block(CarouselBlock())
        self.assertIn('flexslider', html)
