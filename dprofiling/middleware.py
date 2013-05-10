from importlib import import_module
from logging import getLogger
try:
    from cProfile import Profile
except ImportError:
    from Profile import Profile

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.utils import six


from dprofiling.models import ProfileStats


log = getLogger('dprofiling.middleware')



BACKEND = getattr(settings, 'PROFILING_BACKEND',
    'dprofiling.backends.db.DatabaseBackend')
if isinstance(BACKEND, six.string_types):
    _module, _class = BACKEND.rsplit('.', 1)
    _module = import_module(_module)

    BACKEND = getattr(_module, _class)

BACKEND = BACKEND(**getattr(settings,'PROFILING_BACKEND_OPTIONS', {}))

class ProfilingRequestMiddleware(object):
    def enabled(self, request):
        if hasattr(request, '_profiling_enabled'):
            return request._profiling_enabled
        
        count = ProfileStats.on_site.get(path=request.path, active=True).count()

        request._profiling_enabled = False
        if count == 1:
            request._profiling_enabled = True
        elif count > 1:
            log.error('Multiple profile stats active for the requested url')
        return request._profiling_enabled

    def process_request(self, request):
        if self.enabled(request):
            log.debug('Enabling profiling on %s' % (request.path,))
            request._profile = Profile()
            request._profile.enable()
        return None

    def process_response(self, request, response):
        if self.enabled(request):
            request._profile.disable()
            log.debug('Finished profiling of %s' % (request.path,))
            BACKEND.store(request._profile)
            log.debug('Profile information stored for %s' % (request.path,))

        return response

