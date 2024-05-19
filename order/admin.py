from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # Hoặc admin.StackedInline nếu bạn thích dạng hiển thị khác
    model = OrderItem
    extra = 1  # Số lượng form trống để thêm mới

class OrderAdmin(admin.ModelAdmin):
    list_display = ("orderId", "user", "firstName", "lastName", "email", "phone", "address", "payment_mode", "total_price", "status", "created_at")
    inlines = [OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_orderId', 'product', 'price', 'quantity', 'total_price')

    @admin.display(ordering='order__orderId', description='orderId')
    def get_orderId(self, obj):
        return obj.order.orderId

admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
