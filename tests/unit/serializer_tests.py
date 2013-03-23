from django.test import TestCase

from fancypages import loaders
from fancypages.widgets import TextWidget
from fancypages.models import TextWidgetModel


class TestHtmlSerializer(TestCase):

    def setUp(self):
        self.model = TextWidgetModel.objects.create(text='Some strange test')

    def test_can_generate_serialization_for_widget(self):
        widget = loaders.get_widget_for_model(self.model)
        self.assertEquals(widget, TextWidget)
