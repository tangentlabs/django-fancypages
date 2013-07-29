from factory.django import DjangoModelFactory

from django.db.models import get_model

from fancypages.compat import get_user_model


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = 'peter.griffin'
    email = 'peter@griffin.com'


class TextBlockFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'TextBlock')

    text = 'This is a sample text in a text block.'


class HorizontalSeparatorBlockFactory(DjangoModelFactory):
    FACTORY_FOR = get_model('fancypages', 'HorizontalSeparatorBlock')
