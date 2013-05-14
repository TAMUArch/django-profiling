from django.contrib import admin

from dprofiling.models import Session



class SessionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Session, SessionAdmin)

