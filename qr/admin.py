from django.contrib import admin
from qr.models import IdentityAccessRequest, AuthorizedRequester, IdentityAccessPermit

# Register your models here.


# class IdentityViewRequestAdmin(admin.ModelAdmin):
#     list_display = (
#         "request_id",
#         "requester",
#         "created_at",
#         "requested_fields",
#         "is_approved",
#         "is_active",
#     )


# admin.site.register(IdentityViewRequest, IdentityViewRequestAdmin)
admin.site.register(IdentityAccessRequest)
admin.site.register(IdentityAccessPermit)
admin.site.register(AuthorizedRequester)
