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


class CoreConfig(TimeStampedModel):
    app = models.CharField(max_length=20, blank=True)
    description = models.TextField(null=True, blank=True)

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        if self.app:
            return f"{self.app} - {self.key} => {self.value}"
        return f"{self.key} => {self.value}"
