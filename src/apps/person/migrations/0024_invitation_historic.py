# Generated by Django 3.2.15 on 2022-08-22 13:39

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0023_alter_invitation_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='historic',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
