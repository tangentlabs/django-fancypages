from django.core import exceptions
from django.db import IntegrityError

from fancypages import models
from fancypages.test import testcases
from fancypages.utils import get_page_model

FancyPage = get_page_model()


class TestAPage(testcases.FancyPagesTestCase):

    def test_creates_containers_when_saved(self):
        self.prepare_template_file("""{% load fp_container_tags %}
{% block main-content %}
{% fp_object_container first-container %}
{% fp_object_container second-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        page_type = models.PageType.objects.create(
            name="Example Type", template_name=self.template_name)
        article_page = FancyPage.add_root(
            node__name='This is an article', page_type=page_type)

        article_page = FancyPage.objects.get(id=article_page.id)
        self.assertEquals(article_page.containers.count(), 2)


class TestContainer(testcases.FancyPagesTestCase):

    def test_without_page_object_is_unique(self):
        var_name = 'test-container'
        models.Container.objects.create(name=var_name)
        with self.assertRaises(exceptions.ValidationError):
            models.Container.objects.create(name=var_name)

    def test_with_page_object_is_unique(self):
        var_name = 'test-container'
        page = FancyPage.add_root(node__name="Test Page")
        models.Container.objects.create(name=var_name, page_object=page)

        with self.assertRaises(IntegrityError):
            models.Container.objects.create(name=var_name, page_object=page)

    def test_containers_can_have_same_name_for_different_objects(self):
        var_name = 'test-container'
        page = FancyPage.add_root(node__name="Test Page")
        models.Container.objects.create(name=var_name, page_object=page)
        other_page = FancyPage.add_root(node__name="Another Test Page")
        try:
            models.Container.objects.create(
                name=var_name, page_object=other_page)
        except IntegrityError:
            self.fail(
                'containers with different pages do not have to be unique')

    def test_containers_can_have_same_name_with_an_without_object(self):
        var_name = 'test-container'
        page = FancyPage.add_root(node__name="Test Page")
        models.Container.objects.create(name=var_name, page_object=page)
        try:
            models.Container.objects.create(name=var_name)
        except exceptions.ValidationError:
            self.fail(
                'containers with different pages do not have to be unique')
