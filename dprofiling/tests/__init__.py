import unittest

from dprofiling.tests import backends



def suite():
    suite = unittest.TestSuite()
    suite.addTests(backends.suite())
    return suite

