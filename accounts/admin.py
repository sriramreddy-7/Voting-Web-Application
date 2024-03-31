from django.contrib import admin

# Register your models here.
from accounts.models import Organization, Voter

admin.site.register(Organization)
admin.site.register(Voter)