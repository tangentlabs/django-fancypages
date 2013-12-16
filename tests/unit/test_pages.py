from django.core import exceptions
from django.db import IntegrityError
from django.db.models import get_model
from django.template import loader, Context

from fancypages import models
from fancypages.test import testcases
from fancypages.utils import get_container_names_from_template


class TestSwappableModels(testcases.FancyPagesTestCase):

    def test_returns_default_node(self):
        self.assertEquals(
            models.get_node_model(), get_model('fancypages', 'PageNode'))

    def test_returns_default_page(self):
        self.assertEquals(
            models.get_page_model(), get_model('fancypages', 'FancyPage'))


class TestContainerNames(testcases.FancyPagesTestCase):

    def test_can_be_extracted_from_template(self):
        self.prepare_template_file("""{% load fp_container_tags %}
{% block main-content %}
{% fp_object_container first-container %}
{% templatetag opencomment %}
{% endblock %}
{% fp_object_container another-container %}
""")
        self.assertSequenceEqual(
            get_container_names_from_template(self.template_name),
            [u'first-container', u'another-container'])

    def test_cannot_be_duplicated_in_template(self):
        self.prepare_template_file("""{% load fp_container_tags %}
{% block main-content %}
{% fp_object_container first-container %}
{% fp_object_container first-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        with self.assertRaises(exceptions.ImproperlyConfigured):
            get_container_names_from_template(self.template_name)


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
        article_page = models.FancyPage.add_root(
            node__name='This is an article', page_type=page_type)

        article_page = models.FancyPage.objects.get(id=article_page.id)
        self.assertEquals(article_page.containers.count(), 2)


class TestContainer(testcases.FancyPagesTestCase):

    def test_without_page_object_is_unique(self):
        var_name = 'test-container'
        models.Container.objects.create(name=var_name)
        with self.assertRaises(exceptions.ValidationError):
            models.Container.objects.create(name=var_name)

    def test_with_page_object_is_unique(self):
        var_name = 'test-container'
        page = models.FancyPage.add_root(node__name="Test Page")
        models.Container.objects.create(name=var_name, page_object=page)

        with self.assertRaises(IntegrityError):
            models.Container.objects.create(name=var_name, page_object=page)

    def test_containers_can_have_same_name_for_different_objects(self):
        var_name = 'test-container'
        page = models.FancyPage.add_root(node__name="Test Page")
        models.Container.objects.create(name=var_name, page_object=page)
        other_page = models.FancyPage.add_root(node__name="Another Test Page")
        try:
            models.Container.objects.create(
                name=var_name, page_object=other_page)
        except IntegrityError:
            self.fail(
                'containers with different pages do not have to be unique')

    def test_containers_can_have_same_name_with_an_without_object(self):
        var_name = 'test-container'
        page = models.FancyPage.add_root(node__name="Test Page")
        models.Container.objects.create(name=var_name, page_object=page)
        try:
            models.Container.objects.create(name=var_name)
        except exceptions.ValidationError:
            self.fail(
                'containers with different pages do not have to be unique')


class TestContainerWithObject(testcases.FancyPagesTestCase):

    def setUp(self):
        super(TestContainerWithObject, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags %}"
            "{% fp_object_container test-container %}")

        page_type = models.PageType.objects.create(
            name="Example Type", template_name=self.template_name)
        self.page = models.FancyPage.add_root(
            node__name="Some Title", page_type=page_type)
        self.container_names = get_container_names_from_template(
            self.page.page_type.template_name)

    def test_can_be_assigned_to_a_page(self):
        self.assertEquals(self.container_names, [u'test-container'])
        self.assertEquals(self.page.containers.count(), 1)

    def test_cannot_assign_multiple_instance_to_page(self):
        self.assertEquals(self.container_names, [u'test-container'])

        self.page.create_container(self.container_names[0])
        self.assertEquals(self.page.containers.count(), 1)

        self.page.create_container(self.container_names[0])
        self.assertEquals(self.page.containers.count(), 1)

    def test_can_be_retrieved_from_page_and_container_name(self):
        container = models.Container.get_container_by_name(
            name='test-container',
            obj=self.page,
        )
        self.assertEquals(
            container.name,
            self.page.containers.all()[0].name
        )
        self.assertEquals(self.page.containers.count(), 1)


class TestContainerWithoutObject(testcases.FancyPagesTestCase):

    def setUp(self):
        super(TestContainerWithoutObject, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags %}"
            "{% fp_container test-container %}"
        )

    def test_can_be_used_in_template(self):
        tmpl = loader.get_template(self.template_name)
        tmpl.render(Context({}))

        containers = models.Container.objects.all()
        self.assertEquals(len(containers), 1)
        self.assertEquals(containers[0].page_object, None)

    #def test_can_render_contained_blocks(self):
    #    container = models.Container.objects.create(
    #        name='test-container'
    #    )
    #    text = "I am a fancy block with only text"
    #    text_block = models.TextBlock.objects.create(
    #        container=container,
    #        text=text,
    #    )
    #    print self.template_name
    #    tmpl = loader.get_template(self.template_name)
    #    content = tmpl.render(self.client.request().context[0])
    #    self.assertIn(text, content)

    #    container = models.Container.objects.get(id=container.id)
    #    self.assertEquals(container.blocks.count(), 1)
    #    self.assertEquals(container.blocks.all()[0].id, text_block.id)
