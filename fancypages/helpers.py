# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from copy import copy

from django.conf import settings as settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.validators import URLValidator, ValidationError


class BlockFormSettings(dict):

    def __init__(self, **kwargs):
        super(BlockFormSettings, self).__init__(**kwargs)
        self._settings = getattr(settings, 'FP_FORM_BLOCK_CHOICES', {})
        self.mandatory_keys = ('form', 'name', 'url')
        self.url_validator = URLValidator()

        for slug, config in self._settings.iteritems():
            self.validate_keys(config.keys())
            self[slug] = copy(config)

    def validate_keys(self, keys):
        missing_keys = set(self.mandatory_keys) - set(keys)

        # check for missing, mandatory keys
        if missing_keys:
            raise ImproperlyConfigured(
                "missing mandatory keys in form configuration: "
                "{}".format(missing_keys))

    def validate_form(self, config):
        """
        Validate the form class specified as module path in the *config*
        dictionary. Raises ``ImproperlyConfigured`` if class cannot be loaded.
        """
        from fancypages.compat import import_string
        try:
            form_class = import_string(config.get('form'))
        except ImportError:
            raise ImproperlyConfigured(
                "form '{}' doesn't seem to be a valid class".format(
                    config.get('form')))

        return form_class

    def validate_url(self, config):
        """
        Validate the url in *config* to either be a valid URL or a valid
        reverse URL pattern. Relative URLs are only supported throug reverse
        lookup patterns. Raises ``ImproperlyConfigured`` if neither a valid
        URL nor a valid URL pattern can be found.
        """
        try:
            self.url_validator(config.get('url'))
        except ValidationError:
            try:
                url = reverse(config.get('url'))
            except NoReverseMatch:
                raise ImproperlyConfigured(
                    "'{}' is not a valid URL or pattnern name".format(
                        config.get('url')))
        else:
            url = config.get('url')

        return url

    def get_form_class(self, name):
        return self.validate_form(self[name])

    def get_url(self, name):
        return self.validate_url(self[name])

    def as_choices(self):
        for key, config in self.iteritems():
            yield (key, config.get('name'))
