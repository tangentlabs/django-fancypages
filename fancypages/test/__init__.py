import os
import tempfile

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from django_webtest import WebTest


class MockTemplateMixin(object):

    def setUp(self):
        tempdir = tempfile.gettempdir()
        self.default_template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS) + [tempdir]
        self.template_name = 'test_article_page.html'
        self.template_file = os.path.join(tempdir, self.template_name)

    def tearDown(self):
        os.remvoe(self.template_file)
        # make sure that other tests don't rely on these settings
        settings.TEMPLATE_DIRS = self.default_template_dirs

    def prepare_template_file(self, content):
        with open(self.template_file, 'w') as tmpl_file:
            tmpl_file.write(content)


class FancyPagesTestCase(TestCase, MockTemplateMixin):

    def setUp(self):
        super(FancyPagesTestCase, self).setUp()
        MockTemplateMixin.setUp(self)


class FancyPagesWebTest(WebTest, MockTemplateMixin):
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'mysecretpassword'
    is_anonymous = True
    is_staff = False

    def setUp(self):
        super(FancyPagesWebTest, self).setUp()
        MockTemplateMixin.setUp(self)
        self.user = None

        if self.is_staff:
            self.is_anonymous = False

        if self.is_staff or not self.is_anonymous:
            self.user = User.objects.create_user(username=self.username,
                                                 email=self.email,
                                                 password=self.password)
            self.user.is_staff = self.is_staff
            self.user.save()

    def get(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.post(*args, **kwargs)
