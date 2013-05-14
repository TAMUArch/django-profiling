import unittest

from django import test
from django.contrib.sites.models import get_current_site



class DatabaseBackendTestCase(test.TestCase):
    fixtures = ['dprofiling/test.json']

    def test_false(self):
        self.assertEquals(1,2)

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DatabaseBackendTestCase))
    return suite
