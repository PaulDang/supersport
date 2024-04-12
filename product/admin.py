from django.contrib import admin
from .models import Category, Product, ProductDetail
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)