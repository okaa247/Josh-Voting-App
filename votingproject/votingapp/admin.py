from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Userprofile)
class userprof(admin.ModelAdmin):
    list_display = ('fullname', 'dob', 'email', 'address')

@admin.register(VotingCategory)
class votingcat(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Candidate)
class candidates(admin.ModelAdmin):
    list_display = ('name', 'votes_count', 'voting_category')

@admin.register(Payment)
class payments(admin.ModelAdmin):
    list_display = ('amount', 'user', 'email', 'ref', 'verified')
