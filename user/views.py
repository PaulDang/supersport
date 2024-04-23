from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterForm, ChangePasswordForm, UpdateUserForm, UpdatedForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User
from product.models import Product

User = get_user_model()

def cart(request):
    return render(
        request=request,
        template_name="cart.html",
    )


def main(request):
    all_products = Product.objects.all()
    context = {"all_products": all_products}
    return render(request, "product/store.html", context)


def get_signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                login(request, user)
                messages.success(request, "Đăng ký thành công.")
                return redirect("main")

        messages.error(request, "Đăng ký không thành công. Thông tin không hợp lệ.")
    form = RegisterForm()
    return render(
        request=request,
        template_name="signup.html",
        context={"register_form": form},
    )


def get_signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(
                    request, f"Bây giờ bạn đã đăng nhập với tư cách {username}."
                )

                return redirect("main")

        messages.error(request, "Sai username hoặc password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="signin.html",
        context={"login_form": form},
    )


def get_signout(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công.")
    return redirect("signin")


@login_required(login_url="signin")
def update_user_info(request):
    if request.method == "POST":
        form = UpdatedForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thông tin người dùng đã được cập nhật thành công!"
            )
            return redirect("user_info")
    else:
        form = UpdatedForm(instance=request.user)
    return render(
        request=request,
        template_name="user-info.html",
        context={"user_info_form": form},
    )


@login_required(login_url="signin")
def dashboard(request):
    if request.user.is_superuser == 1:
        return render(request=request, template_name="dashboard.html")
    return render(
        request=request,
        template_name="./component/user-info/user-info.html",
    )


@login_required(login_url="signin")
def profile(request):
    # update username and password
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Thông tin đã được cập nhật!")  # Thêm dòng này
            return redirect("profile")
        else:
            messages.error(request, "Vui lòng thử lại.")
    user_form = UpdateUserForm(instance=request.user)
    context = {"user_form": user_form}

    if request.user.is_superuser == 1:
        return render(
            request=request, template_name="profile-management.html", context=context
        )
    return render(
        request=request,
        template_name="./component/user-info/profile-management.html",
        context=context,
    )

@login_required(login_url="signin")
def delete_account(request):
    user = User.objects.get(userId=request.user.userId)
    if request.method == "POST":
        user.delete()
        return redirect("main")
    return render(
        request=request,
        template_name="delete-account.html",
    )


def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            # Xử lý dữ liệu form ở đây
            messages.success(request, "Mật khẩu đã được thay đổi.")
            return redirect("signout")
        else:
            messages.error(request, "Vui lòng thử lại.")
    else:
        # Nếu không phải yêu cầu POST, hiển thị form trống
        form = ChangePasswordForm()
    if request.user.is_superuser == 1:
        return render(
            request=request,
            template_name="change-password.html",
            context={"form": form},
        )
    return render(
        request=request,
        template_name="./component/user-info/change-password.html",
        context={"form": form},
    )
