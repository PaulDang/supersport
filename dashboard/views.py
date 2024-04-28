from django.contrib.auth.decorators import login_required
from user.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import CreateUserForm


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
    users = User.objects.all()
    context = {"users": users, "createUserForm": CreateUserForm()}
    return render(request, "user/user.html", context)


def create_user_dashboard(request):
    context = {"forms": CreateUserForm}
    return render(request, "user/create_form.html", context)


@login_required(login_url="signin")
@require_POST
def delete_user(request, user_id):
    user = User.objects.get(userId=user_id)
    user.delete()
    messages.success(request, "Xóa user thành công.")

    return redirect("user_dashboard")


@login_required(login_url="signin")
@require_POST
def create_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                messages.success(request, "Tạo người dùng thành công.")
                return redirect("user_dashboard")

        messages.error(request, "Tạo người dùng không thành công. Vui lòng thử lại.")
        return redirect("create_user_dashboard")
