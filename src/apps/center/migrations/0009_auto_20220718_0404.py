# Generated by Django 3.2.13 on 2022-07-18 07:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('center', '0008_auto_20220718_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='zip_code',
            field=models.CharField(blank=True, max_length=15, verbose_name='zip'),
        ),
        migrations.AlterField(
            model_name='responsible',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='center.center', verbose_name='center'),
        ),
        migrations.AlterField(
            model_name='responsible',
            name='rule',
            field=models.CharField(choices=[('BDG', 'Badge'), ('SCR', 'Secretary')], default='BDG', max_length=3, verbose_name='rule'),
        ),
        migrations.AlterField(
            model_name='responsible',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]