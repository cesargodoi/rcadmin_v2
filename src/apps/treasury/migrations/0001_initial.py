# Generated by Django 4.2.13 on 2024-06-26 11:35

import apps.treasury.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("event", "0001_initial"),
        ("person", "0001_initial"),
        ("center", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BankFlags",
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
                ("name", models.CharField(max_length=15, verbose_name="name")),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
            ],
            options={
                "verbose_name": "bank and flag",
                "verbose_name_plural": "banks and flags",
            },
        ),
        migrations.CreateModel(
            name="FormOfPayment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "payform_type",
                    models.CharField(
                        choices=[
                            ("PIX", "pix"),
                            ("CSH", "cash"),
                            ("CHK", "check"),
                            ("PRE", "pre check"),
                            ("DBT", "debit"),
                            ("CDT", "credit"),
                            ("DPT", "deposit"),
                            ("TRF", "transfer"),
                            ("SLP", "bank slip"),
                        ],
                        default="CSH",
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                (
                    "ctrl_number",
                    models.CharField(
                        blank=True,
                        max_length=36,
                        null=True,
                        verbose_name="control number",
                    ),
                ),
                (
                    "complement",
                    models.CharField(
                        blank=True, max_length=36, null=True, verbose_name="complement"
                    ),
                ),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="value"
                    ),
                ),
                (
                    "voucher_img",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.treasury.models.voucher_img_filename,
                        verbose_name="image",
                    ),
                ),
                (
                    "bank_flag",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="treasury.bankflags",
                        verbose_name="bank flag",
                    ),
                ),
            ],
            options={
                "verbose_name": "form of payment",
                "verbose_name_plural": "form of payments",
            },
        ),
        migrations.CreateModel(
            name="PayTypes",
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
                    "pay_type",
                    models.CharField(
                        choices=[
                            ("MON", "monthly"),
                            ("EVE", "by event"),
                            ("CAM", "campaign"),
                        ],
                        default="MON",
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
            ],
            options={
                "verbose_name": "pay type",
                "verbose_name_plural": "pay types",
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "ref_month",
                    models.DateField(
                        blank=True, null=True, verbose_name="reference month"
                    ),
                ),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="value"
                    ),
                ),
                (
                    "obs",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="observations",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="event.event",
                        verbose_name="event",
                    ),
                ),
                (
                    "paytype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="treasury.paytypes",
                        verbose_name="pay type",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="person.person",
                        verbose_name="person",
                    ),
                ),
            ],
            options={
                "verbose_name": "payment",
                "verbose_name_plural": "payments",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="amount"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CCL", "canceled"),
                            ("PND", "pending"),
                            ("CCD", "concluded"),
                        ],
                        default="PND",
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
                (
                    "self_payed",
                    models.BooleanField(default=False, verbose_name="self payed"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "center",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="center.center",
                        verbose_name="center",
                    ),
                ),
                (
                    "form_of_payments",
                    models.ManyToManyField(
                        to="treasury.formofpayment", verbose_name="form of payments"
                    ),
                ),
                (
                    "made_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="made_by_order",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payments",
                    models.ManyToManyField(
                        to="treasury.payment", verbose_name="payments"
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
                "verbose_name": "order",
                "verbose_name_plural": "orders",
            },
        ),
    ]
