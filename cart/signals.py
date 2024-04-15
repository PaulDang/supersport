from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Cart


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user_id=instance)


@receiver(pre_delete, sender=User)
def delete_user_cart(sender, instance, **kwargs):
    try:
        cart = Cart.objects.get(user_id=instance)
        cart.delete()
    except Cart.DoesNotExist:
        pass
