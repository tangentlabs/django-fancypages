import mock

from django.test import TestCase
from django.core import exceptions
from django.template import loader, Context, RequestContext
from django.template.base import Parser, Token, TOKEN_BLOCK

from fancypages import models
from fancypages.test import testcases, factories
from fancypages.templatetags.fp_container_tags import parse_arguments
from fancypages.utils import get_container_names_from_template, get_page_model

FancyPage = get_page_model()


class TestParsingObjectTokens(TestCase):

    def get_parser_and_token(self, contents):
        token = Token(TOKEN_BLOCK, contents)
        parser = Parser([token])
        return parser, token

    def test_extracts_mandatory_container_name(self):
        parser, token = self.get_parser_and_token(
            "fp_object_container another-container")
        self.assertItemsEqual(
            parse_arguments(parser, token),
            {'container_name': 'another-container'})

    def test_extracts_object_name(self):
        parser, token = self.get_parser_and_token(
            "fp_object_container another-container my_object")
        self.assertItemsEqual(
            parse_arguments(parser, token),
            {'container_name': 'another-container',
             'object_name': 'my_object'})

    def test_extracts_object_name_from_var(self):
        parser, token = self.get_parser_and_token(
            "fp_object_container another-container object_name=my_object")
        self.assertItemsEqual(
            parse_arguments(parser, token),
            {'container_name': 'another-container',
             'object_name': 'my_object'})

    def test_extracts_language_from_var(self):
        parser, token = self.get_parser_and_token(
            "fp_object_container another-container language='en-gb'")
        self.assertItemsEqual(
            parse_arguments(parser, token),
            {'container_name': 'another-container',
             'language': 'en-gb'})

    def test_extracts_all_vars_from_keywords_correctly(self):
        parser, token = self.get_parser_and_token(
            "fp_object_container another-container language='en-gb' "
            "object_name=my_object")
        self.assertItemsEqual(
            parse_arguments(parser, token),
            {'container_name': 'another-container',
             'object_name': 'my_object', 'language': 'en-gb'})

    def test_extracts_all_vars_from_positional_args_correctly(self):
        parser, token = self.get_parser_and_token(
            "fp_object_container another-container my_object en-gb'")
        self.assertItemsEqual(
            parse_arguments(parser, token),
            {'container_name': 'another-container',
             'object_name': 'my_object', 'language': 'en-gb'})


class TestObjectContainerTag(testcases.FancyPagesTestCase):

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


class TestContainerWithObject(testcases.FancyPagesTestCase):

    def setUp(self):
        super(TestContainerWithObject, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags %}"
            "{% fp_object_container test-container %}")

        page_type = models.PageType.objects.create(
            name="Example Type", template_name=self.template_name)
        self.page = FancyPage.add_root(
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
            name='test-container', obj=self.page)
        self.assertEquals(
            container.name, self.page.containers.all()[0].name)
        self.assertEquals(self.page.containers.count(), 1)


class TestContainerWithLanguageCode(testcases.FancyPagesTestCase):

    def setUp(self):
        super(TestContainerWithLanguageCode, self).setUp()
        self.container_name = 'test-container'
        self.page = FancyPage.add_root(node__name="Some Title")

        self.en_container = factories.ContainerFactory(
            name=self.container_name, page_object=self.page,
            language_code='en-gb')

        factories.TextBlockFactory(
            text='LANGUAGE: en-gb', container=self.en_container)

        self.de_container = factories.ContainerFactory(
            name=self.container_name, page_object=self.page,
            language_code='de')

        factories.TextBlockFactory(
            text='LANGUAGE: de', container=self.de_container)

        mock_request = mock.Mock()
        mock_request.user = factories.UserFactory()
        self.context = RequestContext(
            mock_request, {'fancypage': self.page, 'object': self.page})

    def test_can_render_container_with_different_selected_language_code(self):
        self.prepare_template_file(
            "{% load fp_container_tags %}"
            "{% fp_object_container test-container language='de'%}")

        with mock.patch('fancypages.templatetags.fp_container_tags.get_language') as mock_func:
            mock_func.return_value = 'de'
            tmpl = loader.get_template(self.template_name)
            self.assertIn('LANGUAGE: de', tmpl.render(self.context))

    def test_can_render_container_with_selected_language_code(self):
        self.prepare_template_file(
            "{% load fp_container_tags %}"
            "{% fp_object_container test-container %}")

        with mock.patch('fancypages.templatetags.fp_container_tags.get_language') as mock_func:
            mock_func.return_value = 'en-gb'
            tmpl = loader.get_template(self.template_name)
            self.assertIn('LANGUAGE: en-gb', tmpl.render(self.context))

    def test_can_render_container_with_changed_language_code(self):
        self.prepare_template_file(
            "{% load fp_container_tags %}"
            "{% fp_object_container test-container %}")

        with mock.patch('fancypages.templatetags.fp_container_tags.get_language') as mock_func:
            mock_func.return_value = 'de'
            tmpl = loader.get_template(self.template_name)
            self.assertIn('LANGUAGE: de', tmpl.render(self.context))
