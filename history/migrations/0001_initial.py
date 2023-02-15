# Generated by Django 4.1.5 on 2023-02-12 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivityHistory",
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
                    "activity",
                    models.CharField(
                        choices=[
                            ("logged_in", "Logged In"),
                            ("qr_generated", "QR Generated"),
                            ("qr_scanned", "QR Scanned"),
                            (
                                "approved_access_request",
                                "Approved Identity Access Request.",
                            ),
                            ("viewed_shared_details", "Viewed Shared Identity Details"),
                        ],
                        max_length=100,
                    ),
                ),
                ("description", models.CharField(max_length=255)),
                ("fields", models.JSONField(blank=True, null=True)),
                (
                    "user",
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
    ]
