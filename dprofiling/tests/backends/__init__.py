import unittest

from dprofiling.tests.backends import db



def suite():
    suite = unittest.TestSuite()
    suite.addTests(db.suite())
    return suite

