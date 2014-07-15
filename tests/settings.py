# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import sys

from sandbox import settings
from sandbox.settings import common
from fancypages.test import TEMP_MEDIA_ROOT

sys.path.insert(0, os.path.join(os.path.dirname(settings.__file__), '..'))


class TestSettingsMixin(object):
    MEDIA_ROOT = TEMP_MEDIA_ROOT
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'}}


class StandaloneTest(TestSettingsMixin, settings.StandaloneFancypages):
    pass


class OscarTest(TestSettingsMixin, settings.OscarFancypages):
    TEMPLATE_CONTEXT_PROCESSORS = common.Common.TEMPLATE_CONTEXT_PROCESSORS
