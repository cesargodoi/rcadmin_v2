# Generated by Django 3.2.5 on 2021-08-01 20:27

import apps.center.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("center", "0003_auto_20210617_0930"),
    ]

    operations = [
        migrations.AlterField(
            model_name="center",
            name="image",
            field=models.ImageField(
                blank=True,
                default="default_center.jpg",
                upload_to=apps.center.models.center_pics,
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="pix_image",
            field=models.ImageField(
                blank=True,
                default="default_center_pix.jpg",
                upload_to=apps.center.models.center_pix_pics,
            ),
        ),
    ]
