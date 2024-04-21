from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import CheckoutForm

@login_required(login_url='signin')
def checkout(request):
    data = [{'id': 1, 'product_name': 'Ao thun xanh', 'image_url': 'images/cart-item-image1.png', 'price': 250_000, 'quantity': 1},
          {'id': 2, 'product_name': 'Ao thun den', 'image_url': 'images/cart-item-image1.png', 'price': 150_000, 'quantity': 2},
          {'id': 3, 'product_name': 'Ao thun trang', 'image_url': 'images/cart-item-image1.png', 'price': 200_000, 'quantity': 1},
          {'id': 4, 'product_name': 'Ao thun', 'image_url': 'images/cart-item-image1.png', 'price': 200_000, 'quantity': 1
          }]
    total_price = 0
    for item in data:
        item_total = item['price'] * item['quantity']
        item['item_total'] = item_total
        total_price = total_price + item_total
    
    template = loader.get_template('checkout.html')
    context = {
        'data': data,
        'total_price': total_price
    }

    return HttpResponse(template.render(context, request))

@login_required(login_url='signin')
def placeorder(request):
    data = [{'id': 1, 'product_name': 'Ao thun xanh', 'image_url': 'images/cart-item-image1.png', 'price': 250_000, 'quantity': 1},
          {'id': 2, 'product_name': 'Ao thun den', 'image_url': 'images/cart-item-image1.png', 'price': 150_000, 'quantity': 2},
          {'id': 3, 'product_name': 'Ao thun trang', 'image_url': 'images/cart-item-image1.png', 'price': 200_000, 'quantity': 1},
          {'id': 4, 'product_name': 'Ao thun', 'image_url': 'images/cart-item-image1.png', 'price': 200_000, 'quantity': 1
          }]

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

def aboutus(request):
    template = loader.get_template('aboutus.html')
    return HttpResponse(template.render())

def contactus(request):
    template = loader.get_template('contactus.html')
    return HttpResponse(template.render())
