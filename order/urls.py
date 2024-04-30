from django.urls import path
from . import views

urlpatterns = [
    path("main/checkout", views.checkout, name= "checkout"),
    path("main/placeorder", views.placeorder, name= "placeorder"),
    path("main/order-summary", views.ordersummary, name= "ordersummary"),
    path("main/about-us", views.aboutus, name= "aboutus"),
    path("main/contact-us", views.contactus, name= "contactus"),
]