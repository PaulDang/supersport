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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'images':
            kwargs['widget'] = admin.MultipleImageWidget
            return admin.ModelAdmin.formfield_for_dbfield(self, db_field, **kwargs)
        return super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def save_form(self, request, form, instance):
        form.save()
        if request.FILES.get('images'):
            for image_file in request.FILES.getlist('images'):
                product_image = ProductImage.objects.create(
                    image=image_file, product=instance)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}


admin.site.register(ProductDetail)
admin.site.register(ProductImage)
