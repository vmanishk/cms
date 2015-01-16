from django.contrib import admin
from cmsdata import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
#import django_bootstrap_calendar
#from django_bootstrap_calendar import models

# from cmsdata.models import UserProfile

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
# class UserProfileInline(admin.StackedInline):
    # model = models.UserProfile
    # can_delete = False
    # verbose_name_plural = 'profile'

# # Define a new User admin
# class UserAdmin(UserAdmin):
    # inlines = (UserProfileInline, )

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# admin.site.register(models.Student)
# admin.site.register(models.Teacher)
admin.site.register(models.UserProfile)
# admin.site.register(models.VotingTopic)
admin.site.register(models.Course)
#admin.site.register(models.Attendance)
admin.site.register(models.Material)
admin.site.register(models.UserToCalender)


#admin.site.register(django_bootstrap_calendar.models.CalendarEvent)