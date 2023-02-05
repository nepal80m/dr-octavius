# Generated by Django 4.1.5 on 2023-02-05 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("qr", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IdentityAccessPermit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "permit_id",
                    shortuuidfield.fields.ShortUUIDField(
                        blank=True, editable=False, max_length=22, unique=True
                    ),
                ),
                (
                    "permitted_document_code",
                    models.CharField(
                        choices=[("DVL", "DVL"), ("AGE", "AGE")], max_length=50
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("viewer", models.JSONField(blank=True, null=True)),
                (
                    "permitted_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="IdentityAccessApproval",
        ),
    ]
