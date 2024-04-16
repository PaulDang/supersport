from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterForm, UpdatedForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

User = get_user_model()


def main(request):
    return render(request=request, template_name="index.html")


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


def checkout(request):
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render())


def update_user_info(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(userId=request.user.userId)
        
        if request.method == "POST":
            form = UpdatedForm(request.POST or None, instance=current_user)
            if form.is_valid():
                user = request.user

                # Update user information using cleaned data
                user.firstName = form.cleaned_data.get("firstName")
                user.lastName = form.cleaned_data.get("lastName")
                user.email = form.cleaned_data.get("email")
                user.phone = form.cleaned_data.get("phone")
                user.address = form.cleaned_data.get("address")

                # Save the updated user object
                user.save()

                messages.success(
                    request, "Thông tin người dùng đã được cập nhật thành công!"
                )
        form = UpdatedForm(instance=current_user)
        return render(
            request=request,
            template_name="userInfo.html",
            context={"user_info_form": form},
        )
    else:
        messages.error("Bạn phải đăng nhập để chỉnh sửa")
        return redirect("main")
