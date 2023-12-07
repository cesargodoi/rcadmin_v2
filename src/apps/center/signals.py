import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Center
from rcadmin.common import remove_image_from_folder


@receiver(post_delete, sender=Center)
def delete_center_image_and_pix_image(sender, instance, *args, **kwargs):
    if instance.image.name != "default_center.jpg":
        image_path = instance.image.path
        if os.path.exists(image_path):
            remove_image_from_folder(image_path)

    if instance.pix_image.name != "default_center_pix.jpg":
        pix_image_path = instance.pix_image.path
        if os.path.exists(pix_image_path):
            remove_image_from_folder(pix_image_path)


@receiver(pre_save, sender=Center)
def update_center_image(sender, instance, *args, **kwargs):
    try:
        old_instance = Center.objects.get(pk=instance.pk)
    except Exception:
        old_instance = None

    if old_instance and old_instance.image.name != "default_center.jpg":
        is_new_image = old_instance.image != instance.image
        if is_new_image and old_instance.image:
            remove_image_from_folder(old_instance.image.path)

        if not instance.image:
            instance.image.name = "default_center.jpg"


@receiver(pre_save, sender=Center)
def update_center_image_and_pix_image(sender, instance, *args, **kwargs):
    try:
        old_instance = Center.objects.get(pk=instance.pk)
    except Exception:
        old_instance = None

    if old_instance and old_instance.image.name != "default_center_pix.jpg":
        is_new_pix_image = old_instance.pix_image != instance.pix_image
        if is_new_pix_image and old_instance.pix_image:
            remove_image_from_folder(old_instance.pix_image.path)

        if not instance.pix_image:
            instance.pix_image.name = "default_center_pix.jpg"
