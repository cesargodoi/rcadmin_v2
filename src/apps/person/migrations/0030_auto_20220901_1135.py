# Generated by Django 3.2.15 on 2022-09-01 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0029_invitation_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='address',
            field=models.CharField(blank=True, max_length=50, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='complement',
            field=models.CharField(blank=True, max_length=50, verbose_name='complement'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='district',
            field=models.CharField(blank=True, max_length=50, verbose_name='district'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='number',
            field=models.CharField(blank=True, max_length=10, verbose_name='number'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='zip_code',
            field=models.CharField(blank=True, max_length=15, verbose_name='zip'),
        ),
    ]
