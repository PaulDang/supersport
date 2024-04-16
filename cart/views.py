from django.shortcuts import render
from .cart import Cart
from product.models import Product, ProductDetail
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {
        'cart':cart
    })

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        size = request.POST.get('size')
        product_detail_id = request.POST.get('product_detail_id')
        product_detail = get_object_or_404(ProductDetail, id=product_detail_id)
        cart.add(product_detail=product_detail, quantity=product_quantity)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    pass

def cart_update(request):
    pass