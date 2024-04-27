from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.safestring import mark_safe
from django.urls import reverse


# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])


class Product(models.Model):
    product_name = models.CharField(max_length=250, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0)
    total_quantity = models.IntegerField(default=0)
    # anh Tiến kiểm tra dùm em line này xem có work không
    sizes = models.JSONField(default={})

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.sizes:
            self.sizes = {}
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def formatted_description(self):
        return mark_safe(self.description.replace('\n', '<br/>'))

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

    def __generate_sizes_dict(self, data: str):
        data


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return 'image ' + str(self.pk)


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'ProductDetails'

    def __str__(self):
        return f'{self.product.__str__()} - {self.quantity}'

    def save(self, *args, **kwargs):
        # Update total_quantity of the product when saving product detail
        if self.pk is None:  # Create new instance
            super().save(*args, **kwargs)
            self.product.total_quantity += self.quantity
            self.product.save()
        else:  # Update existing instance
            old_quantity = ProductDetail.objects.get(pk=self.pk).quantity
            quantity_change = self.quantity - old_quantity
            self.product.total_quantity += quantity_change
            self.product.save()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Update total_quantity of the product when deleting product detail
        self.product.total_quantity -= self.quantity
        self.product.save()
        super().delete(*args, **kwargs)
