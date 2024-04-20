from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout, name= "checkout"),
    path("placeorder", views.placeorder, name= "placeorder"),
    path("order-summary", views.ordersummary, name= "ordersummary"),
]