from .utils import qr_code_image
from django.dispatch import receiver
from django.db.models.signals import post_save  # Use the correct signal for custom user models
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid='generate_qr_code')
def generate_qr_code(sender, instance, created, **kwargs):
    """Signal handler to generate a QR code when a new user is created."""
    if created:  # Ensure the QR code is only generated for new users, not updates
        qr_code = qr_code_image(instance)
        instance.qr_code = qr_code
        instance.save()  # Save only once after updating the `qr_code` field
        


