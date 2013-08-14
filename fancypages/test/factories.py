import factory

from factory.django import DjangoModelFactory

from django.conf import settings
from django.db.models import get_model

from fancypages.compat import get_user_model


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


class ContainerFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'Container')

    name = 'test-container'


class TextBlockFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'TextBlock')

    text = 'This is a sample text in a text block.'


class HorizontalSeparatorBlockFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'HorizontalSeparatorBlock')
