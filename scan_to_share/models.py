from django.db import models
from shortuuidfield import ShortUUIDField
from core.models import TimeStampedModel

# Create your models here.
class ScanRequest(TimeStampedModel):
    request_id = ShortUUIDField(unique=True)
    requester = models.CharField(max_length=100)
    requested_fields = models.JSONField()
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.request_id)
