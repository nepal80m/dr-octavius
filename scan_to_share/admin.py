from django.contrib import admin
from scan_to_share.models import ScanRequest

# Register your models here.


class ScanRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_id",
        "requester",
        "created_at",
        "requested_fields",
        "is_approved",
        "is_active",
    )


admin.site.register(ScanRequest, ScanRequestAdmin)
