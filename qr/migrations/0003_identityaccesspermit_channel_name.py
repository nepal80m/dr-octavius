# Generated by Django 4.1.5 on 2023-02-05 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qr", "0002_identityaccesspermit_delete_identityaccessapproval"),
    ]

    operations = [
        migrations.AddField(
            model_name="identityaccesspermit",
            name="channel_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
