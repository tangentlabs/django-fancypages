# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pytest

from django.core.exceptions import ImproperlyConfigured

from fancypages.helpers import BlockFormSettings


def test_undefined_form_choices_return_empty_dict(settings):
    settings.FP_FORM_BLOCK_CHOICES = {}
    assert BlockFormSettings() == {}


@pytest.mark.parametrize('cfg', [
    {'form': 'somewhere.Form', 'url': 'test:url'},
    {'form': 'somewhere.Form', 'name': 'contact form'},
    {'name': 'contact form', 'url': 'http://example.com'}])
def test_invalid_form_choices_raise_exception_for_missing_key(cfg, settings):
    settings.FP_FORM_BLOCK_CHOICES = {'default': cfg}
    with pytest.raises(ImproperlyConfigured):
        BlockFormSettings()


def test_form_class_is_returned_for_valid_module_path_for_form(settings):
    settings.FP_FORM_BLOCK_CHOICES = {'default': {
        'form': 'django.forms.Form',
        'name': 'Django Form',
        'url': 'admin:index'}}

    from django.forms import Form
    config = BlockFormSettings()
    assert config['default']['form'] == 'django.forms.Form'
    assert config.get_form_class('default') == Form


def test_exception_raised_for_invalid_module_path_for_form(settings):
    settings.FP_FORM_BLOCK_CHOICES = {'default': {
        'form': 'invalid.module.Form',
        'name': 'Django Form',
        'url': 'admin:index'}}
    with pytest.raises(ImproperlyConfigured):
        form_settings = BlockFormSettings()
        form_settings.get_form_class('default')


@pytest.mark.parametrize('url,expected', [
    ('https://example.com/endpoint/', 'https://example.com/endpoint/'),
    ('admin:index', '/admin/')])
def test_passing_valid_url_or_lookup_returns_valid_url(url, expected,
                                                       settings):
    settings.FP_FORM_BLOCK_CHOICES = {'default': {
        'form': 'django.forms.Form',
        'name': 'Django Form',
        'url': url}}

    config = BlockFormSettings()
    assert config['default']['url'] == url
    assert config.get_url('default') == expected


def test_form_settings_can_be_iterated_as_choices(settings):
    settings.FP_FORM_BLOCK_CHOICES = {}
    config = BlockFormSettings()
    config.update({'default': {'name': 'The Default'}})
    config.update({'test': {'name': 'Another form'}})

    assert tuple(config.as_choices()) == (('default', 'The Default'),
                                          ('test', 'Another form'))
