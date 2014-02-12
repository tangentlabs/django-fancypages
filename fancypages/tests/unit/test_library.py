import mock

from django.forms import Form
from django.test import TestCase
from django.forms.models import modelform_factory

from fancypages import library as lib
from fancypages.models import ContentBlock, TitleTextBlock
from fancypages.models.blocks.content import ImageBlock


class SampleSuperForm(Form):
    pass


class TestRegisteringForm(TestCase):

    def setUp(self):
        super(TestRegisteringForm, self).setUp()
        lib._block_forms = {}

    def test_works_with_form_as_path(self):
        form_path = 'myapp.forms.SuperBlockForm'
        lib.register_block_form(ContentBlock, form_path)

        self.assertEqual(
            lib._block_forms, {ContentBlock.__name__: form_path})

    def test_works_with_form_class(self):
        lib.register_block_form(ContentBlock, SampleSuperForm)

        self.assertEqual(
            lib._block_forms,
            {ContentBlock.__name__:
             'fancypages.tests.unit.test_library.SampleSuperForm'})


class TestGettingFormForModel(TestCase):

    def setUp(self):
        super(TestGettingFormForModel, self).setUp()
        lib._block_forms, lib._imported_form_cache = {}, {}

    def test_returns_registered_form(self):
        block = TitleTextBlock()
        lib._block_forms = {
            'TitleTextBlock': 'fancypages.tests.unit.test_library.SampleSuperForm'}

        form = lib.get_block_form(block.__class__)
        self.assertEqual(form, SampleSuperForm)

    def test_returns_imported_form(self):
        block = TitleTextBlock()

        class MyFancyForm(SampleSuperForm):
            pass

        lib._imported_form_cache = {'TitleTextBlock': MyFancyForm}

        form = lib.get_block_form(block.__class__)
        self.assertEqual(form, MyFancyForm)

    def test_returns_form_class_on_block_class(self):
        block = TitleTextBlock
        block.form_class = SampleSuperForm
        self.assertEqual(lib.get_block_form(block), SampleSuperForm)

    def test_returns_form_class_on_block_class_using_method(self):
        block = TitleTextBlock
        block.get_form_class = mock.Mock(return_value=SampleSuperForm)
        self.assertEqual(lib.get_block_form(block), SampleSuperForm)

    def test_returns_fancypages_form_class(self):
        from fancypages.dashboard import forms
        block = TitleTextBlock
        self.assertEqual(lib.get_block_form(block), forms.TitleTextBlockForm)

    def test_returns_default_generated_form_class(self):
        from fancypages.dashboard import forms
        form = lib.get_block_form(ImageBlock)
        expected_form = modelform_factory(ImageBlock, form=forms.BlockForm)

        self.assertEqual(form.__name__, expected_form.__name__)
        self.assertEqual(form.__module__, expected_form.__module__)
