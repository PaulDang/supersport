from django.contrib.auth.decorators import login_required
from user.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token


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
    context = {
        "users": users,
    }
    return render(request, "user/user.html", context)


@login_required(login_url="signin")
@require_POST
def delete_user(request, user_id):
    user = User.objects.get(userId=user_id)
    user.delete()
    messages.success(request, "Xóa user thành công.")

    return redirect("user_dashboard")
