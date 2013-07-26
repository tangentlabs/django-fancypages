from django.test import TestCase
from django.contrib.auth.models import User

from fancypages.models import Container


class TestAContainer(TestCase):

    def test_can_be_retrieved_by_name(self):
        container = Container.objects.create(name='some-container')
        retrieved_container = Container.get_container_by_name(container.name)
        self.assertEquals(container.id, retrieved_container.id)


class TestAnObjectContainer(TestCase):

    def test_can_be_retrieved_by_name(self):
        user = User.objects.create(username='testuser')
        container = Container.objects.create(name='some-container',
                                             page_object=user)

        retrieved_container = Container.get_container_by_name(container.name,
                                                              user)
        self.assertEquals(container.id, retrieved_container.id)
