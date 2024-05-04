from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Cart, CartDetail
from product.models import Product, ProductDetail
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from json import loads, JSONDecodeError
from django.db.models import Sum
from django.http import QueryDict
from .exceptions import CartDetailException

# Create your views here.


@login_required(login_url='signin')
def cart(request):
    current_user = request.user
    user_products = CartDetail.objects.filter(
        cart__user__username=current_user.username)

    return render(
        request=request,
        template_name="cart/cart.html", context={
            "user_products": user_products
        }
    )
    # return redirect("user_cart", username=user.username)


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
                raise CartDetailException(
                    message="Giỏ hàng người dùng không tồn tại trong cơ sở dữ liệu",
                    status=422)
            request_data = QueryDict(request.body.decode('utf-8'))
            quantity = int(request_data.get('product_quantity'))
            product_detail_id = request_data.get('product_detail_id')
            product_detail = ProductDetail.objects.filter(
                id=product_detail_id).first()
            if not product_detail:
                raise CartDetailException(
                    message="Sản phẩm này không tồn tại",
                    status_code=422)
            total_quantity = product_detail.quantity
            cart_details_with_the_same_product_detail = CartDetail.objects.filter(
                product_detail=product_detail).exclude(cart=None)
            cart_details_with_the_same_product_detail_quantity = cart_details_with_the_same_product_detail.aggregate(
                total_quantity=Sum('quantity'))['total_quantity'] if cart_details_with_the_same_product_detail.count() > 0 else 0
            remained_quantity = total_quantity - \
                cart_details_with_the_same_product_detail_quantity
            quantity_after_add_cart_detail = remained_quantity - quantity
            if quantity_after_add_cart_detail < 0:
                raise CartDetailException(
                    message=f"Số lượng sản phẩm còn lại không đủ",
                    status_code=422,
                    remained_quantity=remained_quantity
                )
            CartDetail.objects.create(
                cart=current_user_cart, quantity=quantity, product_detail=product_detail)
            return JsonResponse({'message': f'Thêm sản phẩm vào giỏ hàng thành công'}, status=201)
        except (JSONDecodeError) as e:
            return JsonResponse({'error': f"{str(e) if e else 'Invalid JSON data'}"}, status_code=400)
        except CartDetailException as e:
            returned_json = dict(e.additional_error_args)
            returned_json.update({"message": e.message})
            return JsonResponse(returned_json, status=e.status_code)
    return JsonResponse({'error': "Method not allowed"}, status=405)


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
                    product_detail=modify_cart_detail.product_detail).exclude(id=modify_cart_detail.id).exclude(cart=None)
                cart_details_with_the_same_product_detail_quantity = cart_details_with_the_same_product_detail.aggregate(
                    total_quantity=Sum('quantity'))['total_quantity'] if cart_details_with_the_same_product_detail.count() > 0 else 0
                new_total_quantity = cart_details_with_the_same_product_detail_quantity + new_quanity
                product_size_quantity = modify_cart_detail.product_detail.quantity
                if new_total_quantity > product_size_quantity:
                    raise CartDetailException(
                        message=f"The product size cannot exceeds {
                            new_quanity}",
                        old_quantity=modify_cart_detail.quantity
                    )
                modify_cart_detail.quantity = new_quanity
            else:
                raise ValueError("Invalid action")

            modify_cart_detail.save()
            modify_cart_detail.product_detail.save()
            return JsonResponse({'message': f'{action.title()} processed successfully'}, status=201)
        except (JSONDecodeError, ValueError) as e:
            return JsonResponse({'message': f"{str(e) if e else 'Invalid JSON data'}"}, status=400)
        except CartDetailException as e:
            returned_json = dict(e.additional_error_args)
            returned_json.update({"message": e.message})
            return JsonResponse(returned_json, status=e.status_code)
    return JsonResponse({'error': "Method not allowed"}, 405)


def redirect_to_checkout(request):
    return redirect("checkout")
