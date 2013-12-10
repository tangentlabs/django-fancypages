import factory
import itertools

from factory.django import DjangoModelFactory

from django.conf import settings
from django.db.models import get_model

from fancypages.compat import get_user_model


PAGE_GROUPS_NAMES = itertools.cycle(['Primary Navigation', 'Footer'])

FancyPage = get_model('fancypages', 'FancyPage')


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = 'peter.griffin'
    email = 'peter@griffin.com'
    is_staff = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
            if create:
                self.save()


class PageTypeFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'PageType')

    name = 'Sample page type'
    slug = 'sample-page-type'
    template_name = settings.FP_DEFAULT_TEMPLATE


class PageGroupFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'PageGroup')

    name = factory.LazyAttribute(lambda a: PAGE_GROUPS_NAMES.next())


class PageFactory(DjangoModelFactory):
    FACTORY_FOR = FancyPage

    depth = 0
    name = factory.Sequence(lambda n: 'Sample page {}'.format(n))
    status = FancyPage.PUBLISHED


class ContainerFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'Container')

    name = 'test-container'


class TextBlockFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'TextBlock')

    text = 'This is a sample text in a text block.'


class HorizontalSeparatorBlockFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'HorizontalSeparatorBlock')
