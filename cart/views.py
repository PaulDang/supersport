from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, CartDetail
from product.models import Product, ProductDetail
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from json import loads, JSONDecodeError

# Create your views here.


@login_required(login_url='signin')
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


def submit_data(request):
    if (request.method == "POST"):
        try:
            request_data = loads(request.body.decode('utf-8'))
            action = request_data.get('action')
            product_detail_id = request_data.get('productDetailId')
            if (not product_detail_id):
                raise ValueError("There are no Product Detail in your request")

            modify_cart_detail = CartDetail.objects.get(
                product_detail__id=product_detail_id)
            if action == 'delete':
                modify_cart_detail.cart_id = None
            elif action == 'update':
                new_quanity = request_data.get('quantity')
                modify_cart_detail.quantity = modify_cart_detail.product_detail.quantity = new_quanity
            else:
                raise ValueError("Invalid action")

            modify_cart_detail.save()
            modify_cart_detail.product_detail.save()
            return JsonResponse({'message': f'{action.title()} processed successfully'})
        except (JSONDecodeError, ValueError) as e:
            return JsonResponse({'message': f"{str(e) if e else 'Invalid JSON data'}"}, status=400)
    return JsonResponse({'error': "Method not allowed"}, 405)


def redirect_to_checkout(request):
    return redirect("checkout")
