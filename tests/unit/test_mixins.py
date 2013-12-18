import mock

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from fancypages import mixins


class TestTemplateNamesModelMixin(TestCase):

    def setUp(self):
        super(TestTemplateNamesModelMixin, self).setUp()
        self.tmpl_lookup = mixins.TemplateNamesModelMixin()
        self.tmpl_lookup._meta = mock.Mock()
        self.tmpl_lookup._meta.module_name = 'testmodel'

    def test_raises_exception_if_not_configured(self):
        with self.assertRaises(ImproperlyConfigured):
            self.tmpl_lookup.get_template_names()

    def test_returns_specified_template_name_from_attribute(self):
        template_name = 'subdir/sample.html'
        self.tmpl_lookup.template_name = template_name
        self.assertEquals(
            self.tmpl_lookup.get_template_names(), [template_name])

    def test_returns_template_name_from_attr_with_language_suffix(self):
        template_name = 'subdir/sample.html'
        self.tmpl_lookup.template_name = template_name
        self.tmpl_lookup.language_code = 'en'

        self.assertEquals(
            self.tmpl_lookup.get_template_names(),
            ['subdir/sample_en.html', template_name])

    def test_returns_template_name_from_attr_with_language_fallback(self):
        template_name = 'subdir/sample.html'
        self.tmpl_lookup.template_name = template_name
        self.tmpl_lookup.language_code = 'en-gb'

        self.assertEquals(
            self.tmpl_lookup.get_template_names(),
            ['subdir/sample_en-gb.html', 'subdir/sample_en.html',
             template_name])

    def test_returns_templates_with_string_formatting(self):
        template_name = 'subdir/sample_{module_name}.html'
        self.tmpl_lookup.template_name = template_name
        self.assertEquals(
            self.tmpl_lookup.get_template_names(),
            ['subdir/sample_testmodel.html'])

    def test_returns_templates_with_defaults_and_formatting(self):
        template_names = [
            'subdir/sample_{module_name}.html', 'sub2/other.html']
        self.tmpl_lookup.default_template_names = template_names
        self.assertEquals(
            self.tmpl_lookup.get_template_names(),
            ['subdir/sample_testmodel.html', 'sub2/other.html'])

    def test_returns_templates_with_defaults_format_and_language(self):
        template_names = [
            'subdir/sample_{module_name}.html', 'sub2/other.html']
        self.tmpl_lookup.default_template_names = template_names
        self.tmpl_lookup.language_code = 'en-gb'

        self.assertEquals(
            self.tmpl_lookup.get_template_names(),
            ['subdir/sample_testmodel_en-gb.html',
             'subdir/sample_testmodel_en.html',
             'subdir/sample_testmodel.html',
             'sub2/other_en-gb.html',
             'sub2/other_en.html',
             'sub2/other.html'])
