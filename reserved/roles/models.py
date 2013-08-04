#!/usr/bin/env python 
#-*- coding: utf-8 -*- 
from django.db import models

# Create your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE = (
        (0, u'顾客'),
        (1, u'管理员'),
        )

    user = models.OneToOneField(User)
    role = models.IntegerField(u'角色', default=0, choices=USER_TYPE)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
