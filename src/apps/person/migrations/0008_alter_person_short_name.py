# Generated by Django 3.2.14 on 2022-08-08 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0007_auto_20211108_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='short_name',
            field=models.CharField(blank=True, editable=False, max_length=80, null=True),
        ),
    ]
