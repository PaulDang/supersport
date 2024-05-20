from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction
from django.template.defaultfilters import slugify

from product.models import ProductImage, ProductDetail, Brand, Product, Category
from user.models import User
from .forms import CreateUserForm, EditUserForm, ProductForm, ProductImageForm, ProductDetailForm, BrandForm, \
    CategoryForm


def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff
def handle_errors(form, request):
    form_errors = list(form.errors.values())
    error_messages = [" ".join(errors) for errors in form_errors]
    for error_message in error_messages:
        messages.error(request, error_message)


# Create your views here.
@login_required(login_url="signin")
@user_passes_test(is_superuser_or_staff)
def dashboard(request):
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

    return render(request=request, template_name="dashboard.html", context=chart_data)

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
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('brand')
        category_ids = request.POST.getlist('categories')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        brand = Brand.objects.get(id=brand_id)
        categories = Category.objects.filter(id__in=category_ids)
        print(category_ids)
        product = Product(product_name=product_name, brand = brand, description=description,
                          price=price, discount_price=discount_price, total_quantity=0)
        product.save()
        product.categories.set(categories)

        for image_file in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image_file)

        sizes = request.POST.getlist('sizes')
        quantities = request.POST.getlist('quantities')


        for size, quantity in zip(sizes, quantities):
            ProductDetail.objects.create(product=product, size=size, quantity=quantity)

        return  redirect('product_list')
    else:
        product_form = ProductForm()
    return render(request, 'user/upload_product.html',{
        'product_form': product_form
    })

@user_passes_test(is_superuser_or_staff)
def app_brand_add(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_product')  # Redirect to the product upload page after adding a brand
    else:
        form = BrandForm()

    return render(request, 'user/add_brand.html', {'form': form})
@user_passes_test(is_superuser_or_staff)
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save()
            return JsonResponse({'success': True, 'brand_id': brand.id, 'brand_name': brand.brand_name})
    else:
        form = BrandForm()
    return render(request, 'app_brand_add.html', {'form': form})

@user_passes_test(is_superuser_or_staff)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({'success': True, 'category_id': category.id, 'category_name': category.category_name})
    else:
        form = CategoryForm()
    return render(request, 'app_category_add.html', {'form': form})


@user_passes_test(is_superuser_or_staff)
def product_list(request):
    products = Product.objects.all()

    # Truyền danh sách sản phẩm vào template để hiển thị
    return render(request, 'user/all_product.html', {'products': products})
@user_passes_test(is_superuser_or_staff)
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            messages.success(request, 'Sản phẩm đã được xóa thành công.')
        except Product.DoesNotExist:
            messages.error(request, 'Sản phẩm không tồn tại.')
    return redirect('product_list')  # Redirect to the product list page