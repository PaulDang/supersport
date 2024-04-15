from user.models import User
from product.models import ProductDetail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Cart, CartDetail


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def delete_user_cart(sender, instance, **kwargs):
    try:
        cart = Cart.objects.get(user__userId=instance.userId)
        cart.delete()
    except Cart.DoesNotExist:
        pass


# @receiver(post_save, sender=ProductDetail)
# def create_new_product_detail(sender, instance, created, **kwargs):
#     if created:
#         current_user = request.user
#         CartDetail.objects.create(cart=instance)


# @receiver(pre_delete, sender=ProductDetail)
# def delete_product_detail(sender, instance, **kwargs):
#     try:
#         cart = Cart.objects.get(user__userId=instance.userId)
#         cart.delete()
#     except Cart.DoesNotExist:
#         pass
