# Generated by Django 3.2.15 on 2022-08-15 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0010_remove_center_secretary'),
        ('person', '0014_auto_20220814_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempregofperson',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='center.center', verbose_name='center'),
        ),
    ]
