from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from autho.models import OTPToken

User = get_user_model()


# admin.site.register(User, UserAdmin)


class OTPTokenAdmin(admin.ModelAdmin):
    list_display = ("otp", "user", "created_at", "is_active")


admin.site.register(User)
admin.site.register(OTPToken, OTPTokenAdmin)
# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)
# Register onthersmodels
