import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import FormOfPayment
from rcadmin.common import remove_image_from_folder


@receiver(post_delete, sender=FormOfPayment)
def delete_voucher_img(sender, instance, *args, **kwargs):
    if hasattr(instance, "voucher_img") and instance.voucher_img:
        voucher_img_path = instance.voucher_img.path
        if os.path.exists(voucher_img_path):
            remove_image_from_folder(voucher_img_path)
