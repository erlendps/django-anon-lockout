from django.contrib import admin
from anon_lockout.models import AccessSession, Lockout

# Register your models here.
admin.site.register(AccessSession)
admin.site.register(Lockout)
