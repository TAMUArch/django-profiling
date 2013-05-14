from django.contrib import admin

from dprofiling.models import Session, Profile



class SessionAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Session, SessionAdmin)
admin.site.register(Profile, ProfileAdmin)

