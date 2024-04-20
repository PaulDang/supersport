from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterForm, ChangePasswordForm, UpdateUserForm
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
    context = {
        'all_products': all_products
    }
    return render(request, 'product/store.html', context)

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

@login_required(login_url='signin')
def update_user_info(request):
    if request.method == "POST":
        form = UpdatedForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Thông tin người dùng đã được cập nhật thành công!")
            return redirect("user_info")
    else:
        form = UpdatedForm(instance=request.user)
    return render(
        request=request,
        template_name="userInfo.html",
        context={"user_info_form": form},
    )
@login_required(login_url='signin')
def dashboard(request):
    return render(
        request=request,
        template_name="dashboard.html",
    )
@login_required(login_url='signin')
def profile(request):

    # update username and password
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Thông tin đã được cập nhật!')  # Thêm dòng này
            return redirect("profile")
        else:
            messages.error(request, "Vui lòng thử lại. Có thể email đã tồn tại")
    user_form = UpdateUserForm(instance=request.user)
    context = {"user_form": user_form}
    return render(
        request=request,
        template_name="profile-management.html",context=context
    )

@login_required(login_url='signin')
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
            return redirect('signout')
        else:
            messages.error(request, "Vui lòng thử lại.")
    else:
        # Nếu không phải yêu cầu POST, hiển thị form trống
        form = ChangePasswordForm()
    return render(request, 'change-password.html', {'form': form})
