from django.db import models
from product.models import ProductDetail
from user.models import User

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product_detail = models.ForeignKey(
        ProductDetail, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Cart Details"
