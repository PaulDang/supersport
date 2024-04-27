from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('submit_data', views.submit_data, name='cart_submit_data'),
    path('cart_add', views.cart_add, name='cart-add')
]
