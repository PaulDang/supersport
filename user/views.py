from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterForm, UpdateUserForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User
from product.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

User = get_user_model()


def handle_errors(form, request):
    form_errors = list(form.errors.values())
    error_messages = [" ".join(errors) for errors in form_errors]
    for error_message in error_messages:
        messages.error(request, error_message)


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

        handle_errors(form, request)

    form = RegisterForm()
    return render(
        request=request,
        template_name="signup.html",
        context={"register_form": form},
    )


def get_signin(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
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

        handle_errors(form, request)

    form = CustomAuthenticationForm()
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
def profile(request):
    # update username and password
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Thông tin đã được cập nhật!")
            return redirect("profile")

        handle_errors(user_form, request)
    user_form = UpdateUserForm(instance=request.user)
    context = {"user_form": user_form}

    if request.user.is_superuser == 1:
        return render(
            request=request, template_name="profile-management.html", context=context
        )
    return render(
        request=request,
        template_name="./component/profile/profile-management.html",
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


class MyPasswordChangeView(PasswordChangeView):
    template_name = "./component/reset-password/password-change.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Mật khẩu đã được thay đổi. Vui lòng đăng nhập lại!"
        )
        return response


class MyPasswordChangeViewAdmin(PasswordChangeView):
    template_name = "password-change-admin.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Mật khẩu đã được thay đổi. Vui lòng đăng nhập lại!"
        )
        return response
