from django.db import models


# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=250, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='images/', blank=True)
    total_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.__str__()} - {self.quantity}'