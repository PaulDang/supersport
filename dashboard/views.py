from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import User


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
