# Generated by Django 3.2.5 on 2021-08-01 20:27

from django.db import migrations, models
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_auto_20210617_0826"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="default_profile.jpg",
                upload_to=apps.user.models.profile_pics,
            ),
        ),
    ]
