from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'description', 'profile_icon', 'profile_banner')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'name', 'is_staff')


class TrophyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class TrophyUserRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'trophy')


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Trophy, TrophyAdmin)
admin.site.register(models.TrophyUserRelation, TrophyUserRelationAdmin)
