from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user-info/", views.dashboard, name="user-info"),
    path("dashboard/user/", views.user_dashboard, name="user_dashboard"),
]
