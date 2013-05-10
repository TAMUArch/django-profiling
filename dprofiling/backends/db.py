from logging import getLogger
from os import unlink
from tempfile import mkstemp

from django.core.exceptions import MultipleObjectsReturned
from django.core.files import File

from dprofiling.models import ProfileStats, Profile



log = getLogger('dprofiling.backends.db')

class DatabaseBackend(object):
    def __init__(self, local=True, **kwargs):
        self.local = local
        self.tempdir = kwargs.get('tempdir', None)

    def store(self, path, profile):
        temp = None
        try:
            stats = ProfileStats.on_site.get(path=path, active=True)
        except ProfileStats.DoesNotExist, MultipleObjectsReturned:
            log.exception('Error retrieving the profile stats object for %s' %
                    (path,))
        try:
            temp = mkstemp(dir=self.tempdir)
            log.debug('Temporary file created: %s' % (temp.name,))
            profile.dump_stats(temp.name)
            log.debug('Profile information dumped to temporary file')
            stored_profile = Profile(stats=stats, dump=File(temp))
            stored_profile.save()
            log.debug('Profile %d created' % (stored_profile.pk,))
        finally:
            if temp:
                temp.close()
                unlink(temp.name)


        
