# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    Profile, Announcement, Soldier, SoldierDetail, Sol_User_rel, Counsel,
    Approval, ApprovalUnit
)
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class SoldierDetailInline(admin.StackedInline):
    model = SoldierDetail

class SoldierAdmin(admin.ModelAdmin):
    inlines = [
        SoldierDetailInline,
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Announcement)
admin.site.register(Soldier, SoldierAdmin)
admin.site.register(Sol_User_rel)
admin.site.register(Counsel)
admin.site.register(Approval)
admin.site.register(ApprovalUnit)
