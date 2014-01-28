from django.test import TestCase
from django.core.management import call_command

from fancypages.test import factories
from fancypages.utils import get_page_model


class TestPageCreateCommand(TestCase):

    #@skipUnless(settings.USE_OSCAR_SANDBOX,
    #            "test requires django-oscar to be configured.")
    def test_creates_pages_for_category_nodes(self):
        nodes = [factories.PageNodeFactory(), factories.PageNodeFactory()]

        FancyPage = get_page_model()
        self.assertEqual(FancyPage.objects.count(), 0)

        call_command('fp_create_pages_for_nodes')

        self.assertEqual(FancyPage.objects.count(), 2)
        self.assertItemsEqual([p.node for p in FancyPage.objects.all()], nodes)
