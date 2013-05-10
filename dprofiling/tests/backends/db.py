import unittest

from django import test
from django.contrib.sites.models import get_current_site



class DatabaseBackendTest(test.TestCase):
    fixtures = ['dprofiling/test.json']

    def setUp(self):
        pass


    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DatabaseBackendTest)
