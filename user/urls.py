from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("signin/", views.get_signin, name="signin"),
    path("signup/", views.get_signup, name="signup"),
    path("signout/", views.get_signout, name= "signout"),
    path("checkout/", views.checkout, name= "checkout"),
    path("userInfo/", views.update_user_info, name= "userInfo"),
]
