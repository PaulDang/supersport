from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout, name= "checkout"),
    path("placeorder", views.placeorder, name= "placeorder"),
    path("order-summary", views.get_ordersummary, name= "ordersummary"),
    path("about-us", views.get_aboutus, name= "aboutus"),
    path("contact-us", views.get_contactus, name= "contactus"),
]