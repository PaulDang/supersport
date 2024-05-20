from typing import Any
from django.forms import ModelForm
from django import forms
from .models import Order

class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            "firstName",
            "lastName",
            "email",
            "phone",
            "address"
        ]
    
    def clean(self):
        super(CheckoutForm, self).clean()
        # firstName = self.cleaned_data.get('firstName')
        # lastName = self.cleaned_data.get('lastName')
        # email = self.cleaned_data.get('email')
        # phone = self.cleaned_data.get('phone')
        # address = self.cleaned_data.get('address')

        return self.cleaned_data


