# Generated by Django 4.2.13 on 2024-06-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("center", "0011_auto_20221001_1110"),
    ]

    operations = [
        migrations.AlterField(
            model_name="center",
            name="address",
            field=models.CharField(blank=True, max_length=100, verbose_name="address"),
        ),
        migrations.AlterField(
            model_name="center",
            name="number",
            field=models.CharField(blank=True, max_length=25, verbose_name="number"),
        ),
    ]
