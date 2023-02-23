from django.db import models
from shortuuidfield import ShortUUIDField
from core.models import TimeStampedModel
from autho.models import User

# Create your models here.


class AuthorizedRequester(TimeStampedModel):
    name = models.CharField(max_length=255)
    domain = models.URLField(max_length=255, unique=True)
    logo = models.ImageField(
        upload_to="authorized_requester_logo", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    requested_fields = models.JSONField()


class IdentityAccessRequest(TimeStampedModel):
    request_id = ShortUUIDField(unique=True)
    # requester = models.CharField(max_length=100)
    # requested_fields = models.JSONField()
    channel_name = models.CharField(max_length=255)
    requester = models.ForeignKey(AuthorizedRequester, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.request_id)


PERMITTED_DOCUMENT_CODE_CHOICES = [
    ("DVL", "DVL"),
    ("AGE", "AGE"),
]


class IdentityAccessPermit(TimeStampedModel):
    permit_id = ShortUUIDField(unique=True)
    channel_name = models.CharField(max_length=255)
    permitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    permitted_document_code = models.CharField(
        max_length=50, choices=PERMITTED_DOCUMENT_CODE_CHOICES
    )
    is_active = models.BooleanField(default=True)
    viewer = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.permit_id)
