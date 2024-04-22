from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("signin/", views.get_signin, name="signin"),
    path("signup/", views.get_signup, name="signup"),
    path("signout/", views.get_signout, name="signout"),
    # path("checkout/", views.checkout, name= "checkout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("delete-account/", views.delete_account, name="delete-account"),
    path("change-password/", views.change_password, name="change-password"),
    path("user-info/", views.dashboard, name="user-info"),
]
