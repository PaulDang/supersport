from django.contrib import admin
from django import forms
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

    #     CartDetailInlineFormSet = inlineformset_factory(
    #         Cart, CartDetail, fields=('product_detail', 'quantity'), extra=0)

    #     if self.instance:
    #         self.cartdetail_formset = CartDetailInlineFormSet(
    #             instance=self.instance, queryset=CartDetail.objects.all())
    #     # else:
    #     #     self.cartdetail_formset = CartDetailInlineFormSet(
    #     #         instance=self.instance, queryset=CartDetail.objects.filter())

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if commit:
    #         instance.save()

    #     if hasattr(self, 'cartdetail_formset'):
    #         self.cartdetail_formset.instance = instance
    #         self.cartdetail_formset.save()

    #     return instance


class CartDetailInline(admin.TabularInline):
    model = CartDetail
    extra = 0


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

# Register your models here.


class CartDetailAdmin(admin.ModelAdmin):
    list_filter = ("cart", "product_detail")
    list_display = ("cart", "product_detail")
    form = CartDetailAdminForm
    change_form_template = "cart/admin/change_cart_detail_form_with_dynamic_quantity.html"


admin.site.register(Cart, CartAdmin)
admin.site.register(CartDetail, CartDetailAdmin)
