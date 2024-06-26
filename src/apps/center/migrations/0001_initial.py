# Generated by Django 4.2.13 on 2024-06-26 11:34

import apps.center.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Center",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=50, unique=True, verbose_name="name"),
                ),
                (
                    "short_name",
                    models.CharField(
                        blank=True, max_length=25, null=True, verbose_name="short name"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="address"
                    ),
                ),
                (
                    "number",
                    models.CharField(blank=True, max_length=25, verbose_name="number"),
                ),
                (
                    "complement",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="complement"
                    ),
                ),
                (
                    "district",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="district"
                    ),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=50, verbose_name="city"),
                ),
                (
                    "state",
                    models.CharField(blank=True, max_length=2, verbose_name="state"),
                ),
                (
                    "country",
                    models.CharField(
                        choices=[("BR", "Brazil")],
                        default="BR",
                        max_length=2,
                        verbose_name="country",
                    ),
                ),
                (
                    "zip_code",
                    models.CharField(blank=True, max_length=15, verbose_name="zip"),
                ),
                (
                    "phone_1",
                    models.CharField(blank=True, max_length=20, verbose_name="phone"),
                ),
                (
                    "phone_2",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="backup phone"
                    ),
                ),
                ("email", models.CharField(blank=True, max_length=60)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="default_center.jpg",
                        upload_to=apps.center.models.center_pics,
                        verbose_name="image",
                    ),
                ),
                (
                    "pix_image",
                    models.ImageField(
                        blank=True,
                        default="default_center_pix.jpg",
                        upload_to=apps.center.models.center_pix_pics,
                        verbose_name="pix image",
                    ),
                ),
                (
                    "pix_key",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="pix key",
                    ),
                ),
                (
                    "center_type",
                    models.CharField(
                        choices=[
                            ("CNT", "center"),
                            ("CNF", "conference center"),
                            ("CTT", "contact room"),
                        ],
                        default="CNT",
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                (
                    "observations",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="observations",
                    ),
                ),
                ("mentoring", models.BooleanField(default=False)),
                ("treasury", models.BooleanField(default=False)),
                ("publicwork", models.BooleanField(default=False)),
                ("accommodation", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "conf_center",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="center.center",
                        verbose_name="conference center",
                    ),
                ),
                (
                    "made_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="made_by_center",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "center",
                "verbose_name_plural": "centers",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Responsible",
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
                (
                    "rule",
                    models.CharField(
                        choices=[("BDG", "Badge"), ("SCR", "Secretary")],
                        default="BDG",
                        max_length=3,
                        verbose_name="rule",
                    ),
                ),
                (
                    "center",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="center.center",
                        verbose_name="center",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "responsible",
                "verbose_name_plural": "responsibles",
            },
        ),
        migrations.AddField(
            model_name="center",
            name="responsible_for",
            field=models.ManyToManyField(
                blank=True,
                through="center.Responsible",
                to=settings.AUTH_USER_MODEL,
                verbose_name="responsible",
            ),
        ),
    ]
