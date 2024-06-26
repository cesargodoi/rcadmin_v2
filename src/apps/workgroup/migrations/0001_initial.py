# Generated by Django 4.2.13 on 2024-06-26 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("center", "0001_initial"),
        ("person", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
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
                    "role_type",
                    models.CharField(
                        choices=[
                            ("MTR", "mentor"),
                            ("CTT", "contact"),
                            ("MBR", "member"),
                        ],
                        default="MBR",
                        max_length=3,
                        verbose_name="role",
                    ),
                ),
                (
                    "observations",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="person.person",
                        verbose_name="person",
                    ),
                ),
            ],
            options={
                "verbose_name": "membership",
                "verbose_name_plural": "memberships",
            },
        ),
        migrations.CreateModel(
            name="Workgroup",
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
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "workgroup_type",
                    models.CharField(
                        choices=[
                            ("ASP", "aspect"),
                            ("MNT", "maintenance"),
                            ("ADM", "admin"),
                        ],
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "aspect",
                    models.CharField(
                        choices=[
                            ("21", "Project 21"),
                            ("A1", "1st. Aspect"),
                            ("A2", "2nd. Aspect"),
                            ("A3", "3rd. Aspect"),
                            ("A4", "4th. Aspect"),
                            ("GR", "Grail"),
                            ("A5", "5th. Aspect"),
                            ("A6", "6th. Aspect"),
                        ],
                        default="--",
                        max_length=2,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "center",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="center.center",
                        verbose_name="center",
                    ),
                ),
                (
                    "made_by",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="made_by_workgroup",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        through="workgroup.Membership",
                        to="person.person",
                        verbose_name="members",
                    ),
                ),
            ],
            options={
                "verbose_name": "workgroup",
                "verbose_name_plural": "workgroups",
            },
        ),
        migrations.AddField(
            model_name="membership",
            name="workgroup",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="workgroup.workgroup",
                verbose_name="workgroup",
            ),
        ),
    ]
