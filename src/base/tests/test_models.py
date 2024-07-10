from django.test import TestCase

from base.tests.factories import LinkFactory


class LinkModelTest(TestCase):

    def setUp(self):
        self.link = LinkFactory(url='http://www.google.com')

    def test_link_str(self):
        self.assertEqual(str(self.link), self.link.url)

    def test_get_preview(self):
        preview = self.link.get_preview()
        self.assertTrue(preview)
        self.assertEqual(preview.site_name, 'www.google.com')
        self.assertEqual(preview.title, 'Google')
