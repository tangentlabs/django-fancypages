from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from fancypages import test


class TestAnImageAsset(test.FancyPagesWebTest):
    is_staff = True

    def test_cannot_be_uploaded_using_get_request(self):
        response = self.get(reverse('fp-dashboard:image-upload'))

        json_data = json.loads(response.content)
        self.assertFalse(json_data['success'])
        self.assertIn('reason', json_data)
