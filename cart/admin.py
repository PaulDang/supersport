from typing import Any
from django.contrib import admin
from django import forms
from django.http import HttpRequest
from imagekit.admin import AdminThumbnail
from django.db import models
from .models import CartDetail, Cart
from user.models import User
from product.models import ProductDetail
from django.db.models import Q
from django.forms.models import inlineformset_factory


class CartAdminForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        is_disabled = True if kwargs.get('instance', None) else False
        self.fields['user'].disabled = is_disabled
        self.fields['user'].widget.attrs['readonly'] = is_disabled
        self.fields['user'].widget.attrs['disabled'] = is_disabled

        current_user_and_user_with_out_cart = User.objects.filter(
            Q(cart__isnull=True) | Q(cart=self.instance))

        self.fields['user'].queryset = current_user_and_user_with_out_cart


class CartDetailInline(admin.TabularInline):
    model = CartDetail
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product_detail':
            cart_id = request.resolver_match.kwargs.get('object_id', None)
            kwargs['queryset'] = ProductDetail.objects.filter(
                cartdetail__isnull=True)
            if cart_id:
                current_cart_queryset = ProductDetail.objects.filter(
                    cartdetail__cart__id=cart_id)
                merged_queryset = (kwargs['queryset'] | current_cart_queryset)
                kwargs['queryset'] = merged_queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CartAdmin(admin.ModelAdmin):
    inlines = [CartDetailInline]
    form = CartAdminForm
    change_form_template = "cart/admin/change_cart_detail_form_with_dynamic_quantity.html"


class CartDetailAdminForm(forms.ModelForm):
    class Meta:
        model = CartDetail
        fields = ['cart', 'product_detail', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cartless_product_detail = ProductDetail.objects.filter(
            cartdetail__isnull=True)
        self.fields['product_detail'].queryset = cartless_product_detail

# Register your models here.


class CartDetailAdmin(admin.ModelAdmin):
    list_filter = ("cart", "product_detail")
    list_display = ("cart", "product_detail")
    form = CartDetailAdminForm
    change_form_template = "cart/admin/change_cart_detail_form_with_dynamic_quantity.html"


admin.site.register(Cart, CartAdmin)
admin.site.register(CartDetail, CartDetailAdmin)
