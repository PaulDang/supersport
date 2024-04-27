from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, CartDetail
from product.models import Product, ProductDetail
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from json import loads, JSONDecodeError
from django.db.models import Sum
from django.http import QueryDict

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


def cart_add(request):
    if (request.method == "POST"):
        try:
            current_user = request.user
            current_user_cart = Cart.objects.filter(user=current_user).first()
            if not current_user_cart:
                raise KeyError(
                    {"message": "Giỏ hàng người dùng không tồn tại trong cơ sở dữ liệu"})
            request_data = QueryDict(request.body.decode('utf-8'))
            quantity = int(request_data.get('product_quantity'))
            product_detail_id = request_data.get('product_detail_id')
            product_detail = ProductDetail.objects.filter(
                id=product_detail_id).first()
            if not product_detail:
                raise KeyError(
                    {"message": "Sản phẩm không tồn tại trong cơ sở dữ liệu"})
            total_quantity = product_detail.quantity
            cart_details_with_the_same_product_detail = CartDetail.objects.filter(
                product_detail=product_detail)
            cart_details_with_the_same_product_detail_quantity = cart_details_with_the_same_product_detail.aggregate(
                total_quantity=Sum('quantity'))['total_quantity'] if cart_details_with_the_same_product_detail.count() > 0 else 0
            remained_quantity = total_quantity - \
                cart_details_with_the_same_product_detail_quantity
            if remained_quantity <= 0:
                raise KeyError({"message": f"Sản phẩm cỡ {product_detail.size} của {
                               product_detail.product.product_name} không đủ"})
            CartDetail.objects.create(
                cart=current_user_cart, quantity=quantity, product_detail=product_detail)
            return JsonResponse({'message': f'Thêm sản phẩm vào giỏ hàng thành công'})
        except (JSONDecodeError, ValueError) as e:
            return JsonResponse({'message': f"{str(e) if e else 'Invalid JSON data'}"}, status=400)
        except KeyError as e:
            return JsonResponse(e.args[0], status=422)
    return JsonResponse({'error': "Method not allowed"}, 405)


def submit_data(request):
    if (request.method == "POST"):
        try:
            request_data = loads(request.body.decode('utf-8'))
            action = request_data.get('action')
            cart_detail_id = request_data.get('cartDetailId')
            if (not cart_detail_id):
                raise ValueError("There is no Cart Detail in your request")

            modify_cart_detail = CartDetail.objects.get(id=cart_detail_id)
            if action == 'delete':
                modify_cart_detail.cart_id = None
            elif action == 'update':
                new_quanity = int(request_data.get('quantity'))
                cart_details_with_the_same_product_detail = CartDetail.objects.filter(
                    product_detail=modify_cart_detail.product_detail).exclude(id=modify_cart_detail.id).exclude(id=None)
                cart_details_with_the_same_product_detail_quantity = cart_details_with_the_same_product_detail.aggregate(
                    total_quantity=Sum('quantity'))['total_quantity'] if cart_details_with_the_same_product_detail.count() > 0 else 0
                new_total_quantity = cart_details_with_the_same_product_detail_quantity + new_quanity
                product_size_quantity = modify_cart_detail.product_detail.quantity
                if new_total_quantity > product_size_quantity:
                    raise KeyError({
                        "message": f"The product size cannot exceeds {new_quanity}",
                        "old_quantity": modify_cart_detail.quantity})
                modify_cart_detail.quantity = new_quanity
            else:
                raise ValueError("Invalid action")

            modify_cart_detail.save()
            modify_cart_detail.product_detail.save()
            return JsonResponse({'message': f'{action.title()} processed successfully'})
        except (JSONDecodeError, ValueError) as e:
            return JsonResponse({'message': f"{str(e) if e else 'Invalid JSON data'}"}, status=400)
        except KeyError as e:
            return JsonResponse(e.args[0], status=422)
    return JsonResponse({'error': "Method not allowed"}, 405)


def redirect_to_checkout(request):
    return redirect("checkout")
