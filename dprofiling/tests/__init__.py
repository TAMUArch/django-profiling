import unittest

from django import test
from django.conf import settings
from django.test.client import Client
from django.test.utils import override_settings
from django.contrib.sites.models import get_current_site

from dprofiling.middleware import Profile



class BaseTestCase(test.TestCase):
    fixtures = ['dprofiling/test.json']
    urls = 'dprofiling.tests.urls'

    def setUp(self, *args, **kwargs):
        super(BaseTestCase, self).setUp(*args, **kwargs)
        self.client = Client()

    def _check_hello(self, response):
        self.assertEqual(response.content, 'Hello World!')
        self.assertEqual(response.status_code, 200)

    def _check_profile(self, response):
        self.assertTrue(hasattr(response, 'profile'))
        self.asserIsInstance(response.profile, Profile)

    def test_valid_session(self):
        """ Singe session for a path """
        response = self.client.get('/a/')
        self._check_hello(response)
        self._check_profile(response)
        return response


    def test_valid_multisession(self):
        """ Multiple sessions for a path, only 1 active """
        response = self.client.get('/b/')
        self._check_hello(response)
        self._check_profile(response)
        return response

    def test_invalid_multisession(self):
        """ Multiple sessions for a path, 2 active """
        response = self.client.get('/c/')
        self._check_hello(response)
        self.assertFalse(hasattr(response, 'profile'))


def suite():
    from dprofiling.tests import backends

    suite = unittest.TestSuite()
    suite.addTests(backends.suite())
    return suite

