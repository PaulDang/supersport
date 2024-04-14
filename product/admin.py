from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.db import models
from .models import Category, Product, ProductDetail, Brand, ProductImage


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    formfield_overrides = {
        models.ImageField: {'widget': AdminThumbnail(image_field='thumbnail')}
    }

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(ProductDetail)
admin.site.register(ProductImage)