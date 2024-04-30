from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from imagekit.admin import AdminThumbnail
from django.db import models
from .models import Category, Product, ProductDetail, Brand, ProductImage

class ImageInline(admin.StackedInline):
    model = ProductImage

class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    extra = 1  # Number of empty inline forms to display

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ImageInline, ProductDetailInline]
    formfield_overrides = {
        models.ImageField: {'widget': AdminThumbnail(image_field='thumbnail')},
    }

    def get_form(self, request, obj=None, **kwargs):
        FormClass = super().get_form(request, obj, **kwargs)
        FormClass.base_fields['total_quantity'].disabled = True
        return FormClass

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["widget"] = CheckboxSelectMultiple()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(ProductImage)
admin.site.register(ProductDetail)
