import mock

from django.test import TestCase

from fancypages.middleware import EditorMiddleware


class TestEditorMiddleware(TestCase):

    def setUp(self):
        super(TestEditorMiddleware, self).setUp()
        self.user = mock.MagicMock()

        self.request = mock.MagicMock()
        self.request.user = self.user

    def test_adds_edit_mode_to_request_for_authenticated_user(self):
        self.user.is_staff = True
        self.user.is_authenticated = mock.MagicMock(return_value=True)

        mw = EditorMiddleware()
        mw.process_request(self.request)

        self.assertTrue(self.request.fp_edit_mode)

    def test_doesnt_add_edit_mode_for_non_staff_user(self):
        self.user.is_staff = False
        self.user.is_authenticated = mock.MagicMock(return_value=True)

        mw = EditorMiddleware()
        mw.process_request(self.request)

        self.assertFalse(self.request.fp_edit_mode)

    def test_doesnt_add_edit_mode_for_unauthenticated_user(self):
        self.user.is_authenticated = mock.MagicMock(return_value=False)

        mw = EditorMiddleware()
        mw.process_request(self.request)

        self.assertFalse(self.request.fp_edit_mode)
