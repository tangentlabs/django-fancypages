import os
import shutil
import tempfile

from django.test import TestCase
from django.core.management import call_command
from django.test.utils import override_settings


TMP_STATIC_DIR = tempfile.mkdtemp()


@override_settings(
    COMPRESS_ENABLED=True,
    COMPRESS_OFFLINE=True,
    COMPRESS_ROOT=TMP_STATIC_DIR
)
class TestOfflineCompression(TestCase):

    def tearDown(self):
        super(TestOfflineCompression, self).tearDown()
        if os.path.exists(TMP_STATIC_DIR):
            shutil.rmtree(TMP_STATIC_DIR)

    def test_(self):
        call_command('compress')
