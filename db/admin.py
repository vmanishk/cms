from django.contrib import admin
from db import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.vote)
admin.site.register(models.Comment)
admin.site.register(models.Poll)
admin.site.register(models.Yes)
admin.site.register(models.No)
admin.site.register(models.Cantsay)