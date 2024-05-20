from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # Hoặc admin.StackedInline nếu bạn thích dạng hiển thị khác
    model = OrderItem
    extra = 1  # Số lượng form trống để thêm mới

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "firstName", "lastName", "email", "phone", "address", "payment_mode", "total_price", "status", "created_at")
    inlines = [OrderItemInline]
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'quantity', 'size')

admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
