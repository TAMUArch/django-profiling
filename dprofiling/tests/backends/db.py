import unittest

from django import test
from django.contrib.sites.models import get_current_site

from dprofiling.tests import BaseTestCase



class DatabaseBackendTestCase(BaseTestCase):
    pass

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DatabaseBackendTestCase))
    return suite
