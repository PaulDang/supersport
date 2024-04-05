import re
import uuid

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200, null=False, blank=False)
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
                raise ValidationError(_("Invalid email format."), code="invalid_email")

        if self.firstName:
            firstName_regex = r"^[a-zA-Z]+$"
            if not re.match(firstName_regex, self.firstName):
                raise ValidationError(
                    _("Invalid first name format."), code="invalid_firstName"
                )

        if self.lastName:
            lastName_regex = r"^[a-zA-Z]+$"
            if not re.match(lastName_regex, self.lastName):
                raise ValidationError(
                    _("Invalid last name format."), code="invalid_lastName"
                )

        if self.phone:
            phone_regex = r"^\+?1?\d{9,15}$"
            if not re.match(phone_regex, self.phone):
                raise ValidationError(
                    _("Invalid phone number format."), code="invalid_phone"
                )
