# Generated by Django 3.2.5 on 2021-08-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('SRV', 'service'), ('CNF', 'conference'), ('MET', 'meeting'), ('OTH', 'other')], default='SRV', max_length=3, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='aspect',
            field=models.CharField(choices=[('--', '--'), ('A1', '1st. Aspect'), ('A2', '2nd. Aspect'), ('A3', '3rd. Aspect'), ('A4', '4th. Aspect'), ('GR', 'Grail'), ('A5', '5th. Aspect'), ('A6', '6th. Aspect')], default='--', max_length=2),
        ),
    ]