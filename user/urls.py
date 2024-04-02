from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('cart/', views.cart, name='cart'),
]