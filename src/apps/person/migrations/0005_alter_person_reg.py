# Generated by Django 3.2.5 on 2021-08-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_auto_20210801_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='reg',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]