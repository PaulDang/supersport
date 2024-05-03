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
    if request.user.is_superuser == 1:
        return render(request=request, template_name="dashboard.html")
    return render(
        request=request,
        template_name="./component/user-info/user-info.html",
    )


def user_dashboard(request):
    user_list = User.objects.all().order_by(F("date_joined").desc())
    search_query = request.GET.get("q", "")

    if search_query:
        user_list = user_list.filter(
            username__icontains=search_query
        )

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
