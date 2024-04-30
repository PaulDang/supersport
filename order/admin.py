from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
  list_display = ("orderId", "user", "firstName", "lastName", "email", "phone", "address", "payment_mode", "total_price", "status", "created_at")

class OrderItemAdmin(admin.ModelAdmin):
  list_display  = ('get_orderId', 'product', 'price', 'quantity')

  @admin.display(ordering='order__orderId', description='orderId')
  def get_orderId(self, obj):
    return obj.order.orderId

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)