# Generated by Django 3.2.16 on 2022-11-22 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0032_invitation_observations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'verbose_name': 'invitation', 'verbose_name_plural': 'invitations'},
        ),
        migrations.AddField(
            model_name='invitation',
            name='sign_lgpd',
            field=models.BooleanField(default=False),
        ),
    ]
