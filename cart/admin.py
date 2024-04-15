from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.db import models
from .models import CartDetail


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_filter = ("cart", "product_detail")

# admin.site.register(Car)
