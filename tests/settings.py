# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import sys

from sandbox import settings
from fancypages.test import TEMP_MEDIA_ROOT

sys.path.insert(0, os.path.join(os.path.dirname(settings.__file__), '..'))


class TestSettingsMixin(object):
    MEDIA_ROOT = TEMP_MEDIA_ROOT


class StandaloneTest(TestSettingsMixin, settings.StandaloneFancypages):
    pass


class OscarTest(TestSettingsMixin, settings.OscarFancypages):
    pass
