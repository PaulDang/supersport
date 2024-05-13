from django.contrib.auth.decorators import login_required
from user.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import CreateUserForm, EditUserForm
from django.db.models import F
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator


# Create your views here.
@login_required(login_url="signin")
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
        messages.error(
            request, "Chỉnh sửa người dùng không thành công. Vui lòng thử lại."
        )
    else:
        form = EditUserForm(instance=user)

    context = {"forms": form, "user": user}
    return render(request, "user/edit_form.html", context)


@login_required(login_url="signin")
@require_POST
def delete_user(request, user_id):
    user = User.objects.get(userId=user_id)
    user.delete()
    messages.success(request, "Xóa người dùng thành công.")

    return redirect("user_dashboard")


def create_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                messages.success(request, "Tạo người dùng thành công.")
                return redirect("user_dashboard")

        messages.error(request, "Tạo người dùng không thành công. Vui lòng thử lại.")

    context = {"forms": CreateUserForm}
    return render(request, "user/create_form.html", context)
