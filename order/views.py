from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import CheckoutForm
from product.models import Product, ProductDetail
from django.urls import resolve


def generate_product_details_object(product_detail: ProductDetail):
    return {
        'id': product_detail.pk,
        'product_name': product_detail.product.product_name,
        'image_url': product_detail.product.images.all()[0].image,
        'price': product_detail.product.price,
        'quantity': product_detail.quantity
    }


def generate_data(request):
    product_details = ProductDetail.objects.filter(
        cartdetail__cart__user=request.user)
    return list(map(generate_product_details_object, product_details))


@login_required(login_url='signin')
def checkout(request):
    if request.method == "POST":
        data = generate_data(request)
        total_price = 0
        for item in data:
            item_total = item['price'] * item['quantity']
            item['item_total'] = item_total
            total_price = total_price + item_total

        template = 'checkout.html'
        context = {
            'data': data,
            'total_price': total_price
        }
        return render(request=request,
                      template_name=template,
                      context=context)


@login_required(login_url='signin')
def placeorder(request):
    data = generate_data(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.payment_mode = request.POST.get('payment_mode')

            total_price = 0
            for item in data:
                item_total = item['price'] * item['quantity']
                item['item_total'] = item_total
                total_price = total_price + item_total

            order.total_price = total_price
            order.save()

            # for item in data:
            #     OrderItem.objects.create(
            #         order=order,
            #         product=item['id'],
            #         price=item['price'],
            #         quantity=item['quantity']
            #     )

            return redirect('/order-summary')

        else:
            return render(request, "checkout.html", {'form': form})
    else:
        form = CheckoutForm(None)
        return render(request, 'checkout.html', {'form': form})


def ordersummary(request):
    template = loader.get_template('ordersummary.html')
    return HttpResponse(template.render())
