# Generated by Django 3.2.13 on 2022-07-18 06:40

import apps.center.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("center", "0007_alter_responsible_rule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="center",
            name="address",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="address"
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="city",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="city"
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="complement",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="complement"
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="conf_center",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="center.center",
                verbose_name="conference center",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="country",
            field=models.CharField(
                choices=[("BR", "Brazil")],
                default="BR",
                max_length=2,
                verbose_name="country",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="district",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="district"
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="image",
            field=models.ImageField(
                blank=True,
                default="default_center.jpg",
                upload_to=apps.center.models.center_pics,
                verbose_name="image",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="name",
            field=models.CharField(
                max_length=50, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="number",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="number"
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="observations",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="observations",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="pix_image",
            field=models.ImageField(
                blank=True,
                default="default_center_pix.jpg",
                upload_to=apps.center.models.center_pix_pics,
                verbose_name="pix image",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="pix_key",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                unique=True,
                verbose_name="pix key",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="responsible_for",
            field=models.ManyToManyField(
                blank=True,
                through="center.Responsible",
                to=settings.AUTH_USER_MODEL,
                verbose_name="responsible",
            ),
        ),
        migrations.AlterField(
            model_name="center",
            name="short_name",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="short name"
            ),
        ),
        migrations.AlterField(
            model_name="responsible",
            name="rule",
            field=models.CharField(
                choices=[("BDG", "Badge"), ("SCR", "Secretary")],
                default="BDG",
                max_length=3,
            ),
        ),
    ]
