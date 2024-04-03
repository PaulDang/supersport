from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("cart/", views.cart, name="cart"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
]
