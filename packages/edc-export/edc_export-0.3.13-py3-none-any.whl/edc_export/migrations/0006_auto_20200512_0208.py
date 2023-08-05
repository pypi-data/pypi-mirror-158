# Generated by Django 3.0.4 on 2020-05-11 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_export", "0005_exportdata_importdata"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exportdata",
            options={"permissions": [("show_export_admin_action", "Show export action")]},
        ),
        migrations.AlterModelOptions(
            name="importdata",
            options={"permissions": [("show_import_admin_action", "Show import action")]},
        ),
        migrations.AlterModelOptions(
            name="plan",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
            },
        ),
    ]
