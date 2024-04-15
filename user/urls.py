from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("cart/", include("cart.urls")),
    path("signin/", views.get_signin, name="signin"),
    path("signup/", views.get_signup, name="signup"),
    path("signout/", views.get_signout, name="signout"),
    path("checkout/", views.checkout, name="checkout"),
]
