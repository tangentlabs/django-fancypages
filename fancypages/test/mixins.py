import os
import tempfile

from django.conf import settings


class MockTemplateMixin(object):

    def setUp(self):
        tempdir = tempfile.gettempdir()
        self.default_template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS) + [tempdir]
        self.template_name = 'test_article_page.html'
        self.template_file = os.path.join(tempdir, self.template_name)

    def tearDown(self):
        if os.path.exists(self.template_file):
            os.remove(self.template_file)
        # make sure that other tests don't rely on these settings
        settings.TEMPLATE_DIRS = self.default_template_dirs

    def prepare_template_file(self, content):
        with open(self.template_file, 'w') as tmpl_file:
            tmpl_file.write(content)
