from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from order.models import Order, OrderItem
from order.forms import CheckoutForm
from cart.models import Cart, CartDetail
from product.models import Product, ProductDetail
from django.urls import resolve


def generate_data(request):
    cart_details = CartDetail.objects.filter(cart__user=request.user)
    return cart_details


@login_required(login_url="signin")
def checkout(request):
    if request.method == "POST":
        data = generate_data(request)
        total_price = 0
        for item in data:
            item_total = item.product_detail.product.discount_price * item.quantity
            total_price = total_price + item_total

        template = "checkout.html"
        context = {'data': data, 'total_price': total_price}
        return render(request=request, template_name=template, context=context)


@login_required(login_url="signin")
def placeorder(request):
    data = generate_data(request)

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.payment_mode = request.POST.get("payment_mode")

            total_price = 0
            for item in data:
                item_total = item.product_detail.product.price * item.quantity
                total_price = total_price + item_total

            order.total_price = total_price
            order.save()

            neworderitems = CartDetail.objects.filter(cart__user=request.user)
            for item in neworderitems:
                OrderItem.objects.create(
                    order=order,
                    product=item.product_detail.product,
                    price=item.product_detail.product.price,
                    quantity=item.quantity
                )

                orderproduct = ProductDetail.objects.filter(
                    product_id=item.product_detail.product_id, size=item.product_detail.size).first()
                orderproduct.quantity = orderproduct.quantity - item.quantity
                orderproduct.save()

            CartDetail.objects.filter(cart__user=request.user).delete()

            return redirect("/order-summary")

        else:
            return render(request, "checkout.html", {"form": form})
    else:
        form = CheckoutForm(None)
        return render(request, "checkout.html", {"form": form})


def get_ordersummary(request):
    return render(request, "ordersummary.html")


def get_aboutus(request):
    return render(request, "aboutus.html")


def get_contactus(request):
    return render(request, "contactus.html")
