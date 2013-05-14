import unittest

from django import test
from django.contrib.sites.models import get_current_site

from dprofiling.models import Session, Profile
from dprofiling.tests import BaseTestCase



class DatabaseBackendTestCase(BaseTestCase):
    def _check_profile_created(self, response):
        session = Session.on_site.get(path=response.request['PATH_INFO'], active=True)
        qs = Profile.objects.filter(session=session)
        self.assertEqual(qs.count(), 1)
        qs.delete()

    def tearDown(self):
        super(DatabaseBackendTestCase, self).tearDown()
        Profile.objects.all().delete()

    def test_valid_session(self):
        """ Single session for a path """
        response = super(DatabaseBackendTestCase, self).test_valid_session()
        self._check_profile_created(response)
        return response

    def test_valid_multisession(self):
        """ Multiple sessions for a path, only 1 active """
        response = super(DatabaseBackendTestCase, self).test_valid_multisession()
        self._check_profile_created(response)
        return response

    def test_not_found(self):
        """ View returns not found """
        response = super(DatabaseBackendTestCase, self).test_not_found()
        self._check_profile_created(response)
        return response


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DatabaseBackendTestCase))
    return suite
