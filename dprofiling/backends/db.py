from logging import getLogger
from os import unlink, fdopen
from tempfile import mkstemp

from django.core.exceptions import MultipleObjectsReturned
from django.core.files import File

from dprofiling.models import Session, Profile



log = getLogger('dprofiling.backends.db')

class DatabaseBackend(object):
    def __init__(self, local=True, **kwargs):
        self.local = local
        self.tempdir = kwargs.get('tempdir', None)

    def store(self, path, profile):
        temp = None
        try:
            session = Session.on_site.get(path=path, active=True)
        except (Session.DoesNotExist, MultipleObjectsReturned) as e:
            log.exception('Error retrieving the profiling session object for %s' %
                    (path,))
        try:
            temp, path = mkstemp(dir=self.tempdir)
            log.debug('Temporary file created: %s' % (path,))
            temp = fdopen(temp)
            profile.dump_stats(path)
            log.debug('Profile information dumped to temporary file')
            stored_profile = Profile(session=session, dump=File(temp))
            stored_profile.save()
            log.debug('Profile %d created' % (stored_profile.pk,))
        except Exception as e:
            log.exception('Exception while storing profile')
        finally:
            try:
                if temp:
                    temp.close()
                    unlink(path)
                    log.debug('Temporary file removed: %s' % (path,))
            except:
                log.exception('Error while removing a temporary file')


