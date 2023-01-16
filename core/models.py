from django.db import models


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# Create your models here.
class TimeStampedModel(CreatedAtModel, models.Model):
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
