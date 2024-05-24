from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from collections import defaultdict
from django.db.models import Q
from datetime import datetime
from order.models import Order, OrderItem
from product.models import ProductImage, ProductDetail, Brand, Product, Category
from cart.models import CartDetail
from user.models import User
from .forms import (
    CreateUserForm,
    EditUserForm,
    ProductForm,
    BrandForm,
    CategoryForm,
)


def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff


def handle_errors(form, request):
    form_errors = list(form.errors.values())
    error_messages = [" ".join(errors) for errors in form_errors]
    for error_message in error_messages:
        messages.error(request, error_message)


@login_required(login_url="signin")
@user_passes_test(is_superuser_or_staff)
def statistic_user(request):
    users = User.objects.all()

    # Biểu đồ trạng thái người dùng
    status_data = {}
    for user in users:
        status = user.is_active if hasattr(user, "is_active") else "Unknown"
        status_data[status] = status_data.get(status, 0) + 1

    status_chart_data = {
        "labels": ["Đang hoạt động", "Đã vô hiệu hóa"],
        "datasets": [
            {
                "label": "Tỉ lệ số người",
                "data": list(status_data.values()),
                "backgroundColor": [
                    "rgb(54, 162, 235)",
                    "rgb(255, 99, 132)",
                ],
                "hoverOffset": 4,
            }
        ],
    }

    # Biểu đồ role người dùng
    role_data = {
        "Quản trị viên": 0,
        "Nhân viên": 0,
        "Khách hàng": 0,
    }

    for user in users:
        if hasattr(user, "is_superuser") and user.is_superuser:
            role = "Quản trị viên"
        elif hasattr(user, "is_staff") and user.is_staff:
            role = "Nhân viên"
        else:
            role = "Khách hàng"

        role_data[role] += 1

    role_chart_data = {
        "labels": ["Quản trị viên", "Nhân viên", "Khách hàng"],
        "datasets": [
            {
                "label": "Tỉ lệ số người",
                "data": list(role_data.values()),
                "backgroundColor": [
                    "rgb(54, 162, 235)",
                    "rgb(255, 205, 86)",
                    "rgb(255, 99, 132)",
                ],
                "hoverOffset": 4,
            }
        ],
    }

    chart_data = {"chart_data": [status_chart_data, role_chart_data]}

    return render(
        request=request, template_name="statistic-user.html", context=chart_data
    )


# Create your views here.
@login_required(login_url="signin")
@user_passes_test(is_superuser_or_staff)
def dashboard(request):
    return product_list(request)


@user_passes_test(is_superuser_or_staff)
def user_dashboard(request):
    user_list = User.objects.all().order_by(F("date_joined").desc())
    search_query = request.GET.get("q", "")

    if search_query:
        user_list = user_list.filter(username__icontains=search_query)

    # Set up pagination
    p = Paginator(user_list, 5)
    page = request.GET.get("page")
    users = p.get_page(page)

    context = {"users": users}
    return render(request, "user/user.html", context)


@user_passes_test(is_superuser_or_staff)
@login_required(login_url="signin")
def edit_user_dashboard(request, user_id):
    user = get_object_or_404(User, userId=user_id)
    if request.method == "POST":
        form = EditUserForm(request.POST or None, instance=user)
        if form.is_valid():
            updated_user = form.save()

            if updated_user is not None:
                messages.success(request, "Chỉnh sửa người dùng thành công.")
                return redirect("user_dashboard")
        handle_errors(form, request)

    else:
        form = EditUserForm(instance=user)

    context = {"forms": form, "user": user}
    return render(request, "user/edit_form.html", context)


@login_required(login_url="signin")
@require_POST
@user_passes_test(is_superuser_or_staff)
def delete_user(request, user_id):
    user = User.objects.get(userId=user_id)
    user.delete()
    messages.success(request, "Xóa người dùng thành công.")

    return redirect("user_dashboard")


@user_passes_test(is_superuser_or_staff)
def create_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                messages.success(request, "Tạo người dùng thành công.")
                return redirect("user_dashboard")

        handle_errors(form, request)

    context = {"forms": CreateUserForm}
    return render(request, "user/create_form.html", context)


def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        brand_id = request.POST.get("brand")
        category_ids = request.POST.getlist("categories")
        description = request.POST.get("description")
        price = request.POST.get("price")
        discount_price = request.POST.get("discount_price")
        brand = Brand.objects.get(id=brand_id)
        categories = Category.objects.filter(id__in=category_ids)
        print(category_ids)
        product = Product(
            product_name=product_name,
            brand=brand,
            description=description,
            price=price,
            discount_price=discount_price,
            total_quantity=0,
        )
        product.save()
        product.categories.set(categories)

        for image_file in request.FILES.getlist("images"):
            ProductImage.objects.create(product=product, image=image_file)

        sizes = request.POST.getlist("sizes")
        quantities = request.POST.getlist("quantities")

        for size, quantity in zip(sizes, quantities):
            ProductDetail.objects.create(
                product=product, size=size, quantity=quantity)

        return redirect("product_list")
    else:
        product_form = ProductForm()
    return render(request, "user/upload_product.html", {"product_form": product_form})


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        print(request.POST)
        product_name = request.POST.get("product_name")
        brand_id = request.POST.get("brand")
        category_ids = request.POST.getlist("categories")
        description = request.POST.get("description")
        price = request.POST.get("price")
        discount_price = request.POST.get("discount_price")
        brand = Brand.objects.get(id=brand_id)
        categories = Category.objects.filter(id__in=category_ids)

        # Update product details
        product.product_name = product_name
        product.brand = brand
        product.description = description
        product.price = price
        product.discount_price = discount_price
        product.categories.set(categories)
        product.save()

        image_ids = request.POST.getlist("image_ids")

        for image_id in image_ids:
            # Kiểm tra xem có tệp mới được tải lên cho ảnh này không
            if f"images_{image_id}" in request.FILES:
                new_image_file = request.FILES[f"images_{image_id}"]

                # Xử lý tệp mới ở đây, ví dụ: cập nhật ảnh trong database
                image = get_object_or_404(ProductImage, id=image_id)
                image.image = new_image_file
                image.save()

            # Xử lý các tệp hình ảnh mới được tải lên
        new_images = request.FILES.getlist("images")
        for new_image_file in new_images:
            # Tạo một ProductImage mới và lưu vào cơ sở dữ liệu
            new_image = ProductImage(product=product, image=new_image_file)
            new_image.save()

        # Store old cart detail
        cart_details = CartDetail.objects.filter(
            product_detail__product=product)

        # Backup current product detail values in a dictionary
        cart_detail_backup = defaultdict(list)
        for cart_detail in cart_details:
            cart_detail_backup[cart_detail.product_detail.size].append(
                cart_detail)

        # Update product details
        ProductDetail.objects.filter(
            product=product
        ).delete()  # Delete existing product details
        sizes = request.POST.getlist("sizes")
        quantities = request.POST.getlist("quantities")

        # Create new product details
        for size, quantity in zip(sizes, quantities):
            ProductDetail.objects.create(
                product=product, size=size, quantity=quantity)

        # Fetch new product details
        new_product_details = ProductDetail.objects.filter(product=product)

        # Create a mapping from size to new ProductDetail
        new_product_detail_map = {pd.size: pd for pd in new_product_details}

        # Update cart details to reference new product details
        for size, cart_details in cart_detail_backup.items():
            new_product_detail = new_product_detail_map.get(size)
            if new_product_detail:
                for cart_detail in cart_details:
                    cart_detail.product_detail = new_product_detail
                    cart_detail.save()

        messages.success(request, "Sản phẩm đã được cập nhật thành công.")
        return redirect("product_list")
    else:
        product_form = ProductForm(instance=product)
        existing_images = ProductImage.objects.filter(product=product)
        existing_details = ProductDetail.objects.filter(product=product)

    return render(
        request,
        "user/update_product.html",
        {
            "product_form": product_form,
            "existing_images": existing_images,
            "existing_details": existing_details,
        },
    )


@user_passes_test(is_superuser_or_staff)
def product_list(request):
    products = Product.objects.all()

    # Truyền danh sách sản phẩm vào template để hiển thị
    return render(request, "user/all_product.html", {"products": products})


@user_passes_test(is_superuser_or_staff)
def delete_product(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            messages.success(request, "Sản phẩm đã được xóa thành công.")
        except Product.DoesNotExist:
            messages.error(request, "Sản phẩm không tồn tại.")
    return redirect("product_list")  # Redirect to the product list page


# Brand
@user_passes_test(is_superuser_or_staff)
def app_brand_add(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save()
            return JsonResponse(
                {"success": True, "brand_id": brand.id,
                    "brand_name": brand.brand_name}
            )
    else:
        form = BrandForm()

    return render(request, "user/add_brand.html", {"form": form})


@user_passes_test(is_superuser_or_staff)
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, "user/brand_manage.html", {"brands": brands})


@user_passes_test(is_superuser_or_staff)
def add_brand(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("brand_list")
    else:
        form = BrandForm()
    return render(request, "user/add_brand.html", {"form": form})


@user_passes_test(is_superuser_or_staff)
def edit_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect("brand_list")
    else:
        form = BrandForm(instance=brand)
    return render(request, "user/edit_brand.html", {"form": form})


@user_passes_test(is_superuser_or_staff)
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == "POST":
        brand.delete()
        return redirect("brand_list")
    return render(request, "user/delete_brand.html", {"brand": brand})


# Category
@user_passes_test(is_superuser_or_staff)
def category_list(request):
    categories = Category.objects.all()
    return render(request, "user/category_manage.html", {"categories": categories})


@user_passes_test(is_superuser_or_staff)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse(
                {
                    "success": True,
                    "category_id": category.id,
                    "category_name": category.category_name,
                }
            )
    else:
        form = CategoryForm()
    return render(request, "app_category_add.html", {"form": form})


@user_passes_test(is_superuser_or_staff)
def add_category_app(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "user/add_category_app.html", {"form": form})


@user_passes_test(is_superuser_or_staff)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "user/edit_category.html", {"form": form})


@user_passes_test(is_superuser_or_staff)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "user/delete_category.html", {"category": category})


#  Quản lý order
@user_passes_test(is_superuser_or_staff)
def order_list(request):
    orders = Order.objects.all()
    status_filter = request.GET.get("status")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if status_filter:
        orders = orders.filter(status=status_filter)

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        orders = orders.filter(created_at__date__gte=start_date)

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        orders = orders.filter(created_at__date__lte=end_date)

    context = {
        "orders": orders,
        "orderstatuses": Order._meta.get_field("status").choices,
        "status_filter": status_filter,
        "start_date": start_date.strftime("%Y-%m-%d") if start_date else "",
        "end_date": end_date.strftime("%Y-%m-%d") if end_date else "",
    }
    return render(request, "user/order_list.html", context)


@user_passes_test(is_superuser_or_staff)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        "order": order,
        "order_items": order_items,
        "orderstatuses": Order._meta.get_field("status").choices,
    }
    return render(request, "user/order_detail.html", context)


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status = request.POST.get("status")
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
        return JsonResponse({"success": True, "status": order.get_status_display()})
    return JsonResponse({"success": False})
