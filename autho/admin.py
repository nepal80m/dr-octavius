from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from autho.models import OTPToken

User = get_user_model()


# class UserAdmin(BaseUserAdmin):
#     list_display = ("id", "name", "phone", "address", "otp", "logged", "count")
#     list_filter = ("staff", "active", "admin", "doctor", "user")
#     fieldsets = (
#         (None, {"fields": ("phone", "password")}),
#         (
#             "Personal info",
#             {
#                 "fields": (
#                     "name",
#                     "address",
#                 )
#             },
#         ),
#         ("Permissions", {"fields": ("admin", "staff", "active", "doctor", "user")}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = ((None, {"classes": ("wide",), "fields": ("phone", "otp")}),)
#     search_fields = ("phone", "name")
#     ordering = ("phone", "name")
#     filter_horizontal = ()

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(UserAdmin, self).get_inline_instances(request, obj)


# admin.site.register(User, UserAdmin)


class OTPTokenAdmin(admin.ModelAdmin):
    list_display = ("otp", "user", "created_at", "is_active")


admin.site.register(User)
admin.site.register(OTPToken, OTPTokenAdmin)
# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)
# Register onthersmodels
