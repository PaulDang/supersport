from django.db import models
from product.models import ProductDetail
from user.models import User

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class CartDetail(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    product_detail = models.OneToOneField(
        ProductDetail, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('cart', 'product_detail')
