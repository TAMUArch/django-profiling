import time

from django.conf import settings

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.http import urlquote



def upload_profile(instance, filename):
    return '%s_%s_%s' % (instance.stats.site.pk, urlquote(instance.stats.path),
            time.time(),)

class ProfileStats(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    path = models.URLField(null=False, blank=False, db_index=True)
    site = models.ForeignKey(Site, null=False, blank=False, db_index=True)
    active = models.BooleanField(default=False, null=False, blank=False,
            db_index=True)


    objects = models.Manager()
    on_site = CurrentSiteManager()

class Profile(models.Model):
    stats = models.ForeignKey(ProfileStats, null=False, blank=False,
            db_index=True)
    dump = models.FileField(null=False, blank=False, max_lenth=255,
            upload_to=getattr('PROFILING_PROFILE_UPLOAD_TO', upload_profile),
            storage=getattr('PROFILING_PROFILE_STORAGE', None))



