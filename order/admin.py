from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
  list_display = ("user", "firstName", "lastName", "email", "phone", "address", "payment_mode", "total_price", "status", "created_at")
  
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)