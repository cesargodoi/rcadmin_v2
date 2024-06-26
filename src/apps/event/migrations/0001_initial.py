# Generated by Django 4.2.13 on 2024-06-26 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("person", "0001_initial"),
        ("center", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
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
                    "activity_type",
                    models.CharField(
                        choices=[
                            ("SRV", "service"),
                            ("CNF", "conference"),
                            ("MET", "meeting"),
                            ("OTH", "other"),
                        ],
                        default="SRV",
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                (
                    "multi_date",
                    models.BooleanField(default=False, verbose_name="multi date"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
            ],
            options={
                "verbose_name": "activity",
                "verbose_name_plural": "activities",
            },
        ),
        migrations.CreateModel(
            name="Event",
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
                ("date", models.DateField(verbose_name="date")),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="end"),
                ),
                (
                    "deadline",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="dead line"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("OPN", "opened"), ("CLS", "closed")],
                        default="OPN",
                        max_length=3,
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
                ("is_active", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="event.activity",
                        verbose_name="activity",
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
            ],
            options={
                "verbose_name": "event",
                "verbose_name_plural": "events",
                "ordering": ["date"],
            },
        ),
        migrations.CreateModel(
            name="Frequency",
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
                        verbose_name="aspect",
                    ),
                ),
                (
                    "observations",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="observations",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="event.event",
                        verbose_name="event",
                    ),
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
                "verbose_name": "frequency",
                "verbose_name_plural": "frequencies",
            },
        ),
        migrations.AddField(
            model_name="event",
            name="frequencies",
            field=models.ManyToManyField(
                blank=True,
                through="event.Frequency",
                to="person.person",
                verbose_name="frequencies",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="made_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_event",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
