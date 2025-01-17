import re
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=254, null=True, blank=True)
    firstName = models.CharField(max_length=200, null=True, blank=True)
    lastName = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

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

    def change_password(self, new_password):
        self.password = make_password(new_password)
        self.save()

    class Meta:
        verbose_name_plural = 'Quản lý người dùng'
