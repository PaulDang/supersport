import re
import uuid
from django.db import models
from user.models import User
from product.models import Product
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    # orderId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=150, null=False, blank=False)
    lastName = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=150, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    orderstatuses = (
        ('Created', 'Đã tạo'),
        ('Shipping', 'Đang vận chuyển'),
        ('Completed', 'Hoàn thành')
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='Created')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.email:
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, self.email):
                raise ValidationError(_("Email không hợp lệ."), code="invalid_email")

        if self.firstName:
            firstName_regex = r"^[a-zA-ZÀ-Ỹà-ỹ\s]+$"
            if not re.match(firstName_regex, self.firstName):
                raise ValidationError(
                    _("Tên không được chứa số hay ký tự đặc biệt."),
                    code="invalid_firstName",
                )

        if self.lastName:
            lastName_regex = r"^[a-zA-ZÀ-Ỹà-ỹ\s]+$"
            if not re.match(lastName_regex, self.lastName):
                raise ValidationError(
                    _("Tên không được chứa số hay ký tự đặc biệt."),
                    code="invalid_lastName",
                )

        if self.phone:
            phone_regex = r"^\+?1?\d{9,15}$"
            if not re.match(phone_regex, self.phone):
                raise ValidationError(
                    _("Số điện thoại không hợp lệ."), code="invalid_phone"
                )
    class Meta:
        verbose_name_plural = 'Đơn hàng'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=True, editable=False)  # Add total_price field
    size = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price  # Calculate total price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Chi tiết đơn hàng'