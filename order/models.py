import re
from django.db import models
from user.models import User
from product.models import Product
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=150, null=False, blank=False)
    lastName = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=150, null=False, validators=[validate_email], blank=False)
    phone = models.CharField(max_length=150, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    orderstatuses = (
        ('Pending', 'Pending'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.email:
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, self.email):
                raise ValidationError(_("Invalid email format."), code="invalid_email")
        
        if self.phone:
            phone_regex = r"^\+?1?\d{9,15}$"
            if not re.match(phone_regex, self.phone):
                raise ValidationError(
                    _("Invalid phone number format."), code="invalid_phone"
                )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

