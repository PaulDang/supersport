from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from order.models import Order, OrderItem
from order.forms import CheckoutForm
from cart.models import CartDetail
from product.models import ProductDetail
from django.http import HttpResponseRedirect
from django.urls import reverse


def generate_data(request):
    cart_details = CartDetail.objects.filter(cart__user=request.user)
    return cart_details

@login_required(login_url="signin")
def checkout(request):
    if request.method == "POST":
        data = generate_data(request)
        total_price = 0

        for item in data:
            standard_price = item.product_detail.product.price
            discount_price = item.product_detail.product.discount_price

            if (discount_price > 0 and discount_price < standard_price):
                price = discount_price
            else:
                price = standard_price

            item_total = price * item.quantity
            total_price = total_price + item_total

        template = "checkout.html"
        # user_info = init_user(request)
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
                standard_price = item.product_detail.product.price
                discount_price = item.product_detail.product.discount_price

                if (discount_price > 0 and discount_price < standard_price):
                    price = discount_price
                else:
                    price = standard_price

                item_total = price * item.quantity
                total_price = total_price + item_total

            order.total_price = total_price
            order.save()

            neworderitems = CartDetail.objects.filter(cart__user=request.user)
            for item in neworderitems:
                standard_price = item.product_detail.product.price
                discount_price = item.product_detail.product.discount_price

                if (discount_price > 0 and discount_price < standard_price):
                    price = discount_price
                else:
                    price = standard_price
                # Tạo New OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=item.product_detail.product,
                    price=price,
                    quantity=item.quantity,
                    size=item.product_detail.size
                )

                # Giảm số lượng product quantity trong Product Detail
                orderedproduct = ProductDetail.objects.filter(
                    product_id=item.product_detail.product_id, size=item.product_detail.size).first()

                orderedproduct.quantity = orderedproduct.quantity - item.quantity
                orderedproduct.save()
            
            # Xóa cart detail
            CartDetail.objects.filter(cart__user=request.user).delete()

            return HttpResponseRedirect(reverse("ordersummary", args=(order.id,)))

            # return redirect("/main/order-summary/", orderId = '123')

        else:
            return render(request, "checkout.html", {"form": form})
    else:
        form = CheckoutForm(None)
        return render(request, "checkout.html", {"form": form})


def get_ordersummary(request, orderId):
    my_order = Order.objects.get(id=orderId)
    order_items = OrderItem.objects.filter(order__id = orderId)
    return render(request, "ordersummary.html", {"order": my_order, "orderItems": order_items})


def get_aboutus(request):
    return render(request, "aboutus.html")


def get_contactus(request):
    return render(request, "contactus.html")
