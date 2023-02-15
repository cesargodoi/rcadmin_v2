# Generated by Django 3.2.14 on 2022-08-09 18:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import apps.publicwork.models


class Migration(migrations.Migration):

    dependencies = [
        ("center", "0010_remove_center_secretary"),
        ("person", "0012_auto_20220809_1525"),
        ("publicwork", "0017_auto_20211009_1024"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicofseeker",
            name="date",
            field=models.DateField(blank=True, null=True, verbose_name="date"),
        ),
        migrations.AlterField(
            model_name="historicofseeker",
            name="description",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="description",
            ),
        ),
        migrations.AlterField(
            model_name="historicofseeker",
            name="occurrence",
            field=models.CharField(
                choices=[
                    ("OBS", "observation"),
                    ("NEW", "new"),
                    ("MBR", "member"),
                    ("INS", "installing"),
                    ("ITD", "installed"),
                    ("STD", "stand by"),
                    ("RST", "restriction"),
                ],
                default="MBR",
                max_length=3,
                verbose_name="occurrence",
            ),
        ),
        migrations.AlterField(
            model_name="historicofseeker",
            name="seeker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="publicwork.seeker",
                verbose_name="seeker",
            ),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="center",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="center.center",
                verbose_name="center",
            ),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="date",
            field=models.DateField(blank=True, null=True, verbose_name="date"),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="description",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="description",
            ),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="listeners",
            field=models.ManyToManyField(
                blank=True,
                through="publicwork.Listener",
                to="publicwork.Seeker",
                verbose_name="listeners",
            ),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="theme",
            field=models.CharField(max_length=100, verbose_name="theme"),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="type",
            field=models.CharField(
                choices=[("CTT", "contact"), ("MET", "meeting")],
                default="CTT",
                max_length=3,
                verbose_name="type",
            ),
        ),
        migrations.AlterField(
            model_name="listener",
            name="lecture",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="publicwork.lecture",
                verbose_name="lecture",
            ),
        ),
        migrations.AlterField(
            model_name="listener",
            name="observations",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="observations",
            ),
        ),
        migrations.AlterField(
            model_name="listener",
            name="ranking",
            field=models.IntegerField(default=0, verbose_name="ranking"),
        ),
        migrations.AlterField(
            model_name="listener",
            name="seeker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="publicwork.seeker",
                verbose_name="seeker",
            ),
        ),
        migrations.AlterField(
            model_name="publicworkgroup",
            name="center",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="center.center",
                verbose_name="center",
            ),
        ),
        migrations.AlterField(
            model_name="publicworkgroup",
            name="description",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="description",
            ),
        ),
        migrations.AlterField(
            model_name="publicworkgroup",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
        migrations.AlterField(
            model_name="publicworkgroup",
            name="members",
            field=models.ManyToManyField(
                blank=True, to="publicwork.Seeker", verbose_name="members"
            ),
        ),
        migrations.AlterField(
            model_name="publicworkgroup",
            name="mentors",
            field=models.ManyToManyField(
                blank=True, to="person.Person", verbose_name="mentors"
            ),
        ),
        migrations.AlterField(
            model_name="publicworkgroup",
            name="name",
            field=models.CharField(max_length=50, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="birth",
            field=models.DateField(
                blank=True, null=True, verbose_name="birth"
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="center",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="center.center",
                verbose_name="center",
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="city",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="city"
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="country",
            field=models.CharField(
                choices=[("BR", "Brazil")],
                default="BR",
                max_length=2,
                verbose_name="country",
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="gender",
            field=models.CharField(
                choices=[
                    ("M", "male"),
                    ("F", "female"),
                    ("-", "do not inform"),
                ],
                default="M",
                max_length=1,
                verbose_name="gender",
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="image",
            field=models.ImageField(
                blank=True,
                default="default_profile.jpg",
                upload_to=apps.publicwork.models.seeker_pics,
                verbose_name="image",
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="name",
            field=models.CharField(max_length=80, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="observations",
            field=models.TextField(blank=True, verbose_name="observations"),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="short_name",
            field=models.CharField(
                blank=True, max_length=40, null=True, verbose_name="short name"
            ),
        ),
        migrations.AlterField(
            model_name="seeker",
            name="status_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="status date"
            ),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="birth",
            field=models.DateField(verbose_name="birth"),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="city",
            field=models.CharField(max_length=50, verbose_name="city"),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="country",
            field=models.CharField(
                choices=[("BR", "Brazil")],
                default="BR",
                max_length=2,
                verbose_name="country",
            ),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="gender",
            field=models.CharField(
                choices=[
                    ("M", "male"),
                    ("F", "female"),
                    ("-", "do not inform"),
                ],
                default="M",
                max_length=1,
                verbose_name="gender",
            ),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="image",
            field=models.ImageField(
                blank=True,
                default="default_profile.jpg",
                upload_to=apps.publicwork.models.seeker_pics,
                verbose_name="image",
            ),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="name",
            field=models.CharField(max_length=80, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="phone",
            field=models.CharField(max_length=20, verbose_name="phone"),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="solicited_on",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="solicited on"
            ),
        ),
        migrations.AlterField(
            model_name="tempregofseeker",
            name="state",
            field=models.CharField(max_length=2, verbose_name="state"),
        ),
    ]
