from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cart, CartDetail
from product.models import Product, ProductDetail

# Create your views here.


def cart(request):
    user = request.user
    return redirect("user_cart", username=user.username)


def cart_view(request, username):
    current_user = request.user
    if username != current_user.username:
        raise Http404()
    user_products = CartDetail.objects.filter(cart__user__username=username)

    return render(
        request=request,
        template_name="cart/cart.html", context={
            "user_products": user_products
        }
    )
