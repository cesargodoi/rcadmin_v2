import os

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import User, Profile
from apps.person.models import Person
from rcadmin.common import remove_image_from_folder


@receiver(post_save, sender=User)
def create_profile_and_person(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_active != instance.person.is_active:
        instance.person.is_active = instance.is_active
        instance.person.save()
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, *args, **kwargs):
    if hasattr(instance, "image") and instance.image:
        if instance.image.name != "default_profile.jpg":
            image_path = instance.image.path
            if os.path.exists(image_path):
                remove_image_from_folder(image_path)


@receiver(pre_save, sender=Profile)
def update_profile_image(sender, instance, *args, **kwargs):
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Exception:
        old_instance = None

    if old_instance and old_instance.image.name != "default_profile.jpg":
        is_new_image = old_instance.image != instance.image
        if is_new_image and old_instance.image:
            remove_image_from_folder(old_instance.image.path)

        if not instance.image:
            instance.image.name = "default_profile.jpg"
