import os

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import TempRegOfSeeker, Seeker, HistoricOfSeeker
from rcadmin.common import remove_image_from_folder


@receiver(post_save, sender=Seeker)
def insert_historic(sender, instance, created, **kwargs):
    if created:
        date = timezone.now().date()
        instance.status = "NEW"
        instance.status_date = date
        instance.save()
        HistoricOfSeeker.objects.create(
            seeker=instance,
            occurrence="NEW",
            date=date,
            description="entered as a new seeker",
            made_by=instance.made_by,
        )


@receiver(post_delete, sender=TempRegOfSeeker)
def delete_temp_reg_of_seeker_image(sender, instance, *args, **kwargs):
    if instance.image.name != "default_profile.jpg":
        image_path = instance.image.path
        if os.path.exists(image_path):
            remove_image_from_folder(image_path)


@receiver(post_delete, sender=Seeker)
def delete_seeker_image(sender, instance, *args, **kwargs):
    if instance.image.name != "default_profile.jpg":
        print("image_.name != default_profile.jpg ")
        image_path = instance.image.path
        if os.path.exists(image_path):
            remove_image_from_folder(image_path)
    else:
        print("image_.name == default_profile.jpg ")
        print()


@receiver(pre_save, sender=Seeker)
def update_seeker_image(sender, instance, *args, **kwargs):
    try:
        old_instance = Seeker.objects.get(pk=instance.pk)
    except Exception:
        old_instance = None

    if old_instance and old_instance.image.name != "default_profile.jpg":
        is_new_image = old_instance.image != instance.image
        if is_new_image and old_instance.image:
            remove_image_from_folder(old_instance.image.path)

        if not instance.image:
            instance.image.name = "default_profile.jpg"
