# Generated by Django 3.2.15 on 2022-08-31 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0028_alter_invitation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='migration',
            field=models.BooleanField(default=False),
        ),
    ]
