# Generated by Django 3.2.5 on 2021-08-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_alter_person_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historic',
            name='occurrence',
            field=models.CharField(choices=[('TRF', 'transfered'), ('RGS', 'regressed'), ('OTH', 'other'), ('PRP', 'preparatório'), ('PRB', 'probatório'), ('PRF', 'professo'), ('--', '--'), ('A1', '1st. Aspect'), ('A2', '2nd. Aspect'), ('A3', '3rd. Aspect'), ('A4', '4th. Aspect'), ('GR', 'Grail'), ('A5', '5th. Aspect'), ('A6', '6th. Aspect'), ('---', '---'), ('ACT', 'active'), ('LIC', 'licensed'), ('DEA', 'dead'), ('DIS', 'disconnected'), ('REM', 'removed')], default='ACT', max_length=3),
        ),
        migrations.AlterField(
            model_name='person',
            name='aspect',
            field=models.CharField(choices=[('--', '--'), ('A1', '1st. Aspect'), ('A2', '2nd. Aspect'), ('A3', '3rd. Aspect'), ('A4', '4th. Aspect'), ('GR', 'Grail'), ('A5', '5th. Aspect'), ('A6', '6th. Aspect')], default='--', max_length=2),
        ),
    ]