from django.contrib import admin

# Register your models here.
from accounts.models import Organization, Voter , Poll, Choice, PollVote

admin.site.register(Organization)
admin.site.register(Voter)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(PollVote)
