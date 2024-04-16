from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('<str:username>/', views.cart_view, name="user_cart")
]
