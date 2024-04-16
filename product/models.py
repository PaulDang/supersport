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
    categories = models.ManyToManyField(Category,blank=True,  null=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0)
    total_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def formatted_description(self):
        return mark_safe(self.description.replace('\n', '<br/>'))

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(100, 50)],
                               format='JPEG',
                               options={'quality': 60})

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