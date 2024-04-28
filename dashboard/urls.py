from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user-info/", views.dashboard, name="user-info"),
    path("dashboard/user/", views.user_dashboard, name="user_dashboard"),
    path(
        "dashboard/user/create",
        views.create_user_dashboard,
        name="create_user_dashboard",
    ),
    path("delete_user/<str:user_id>/", views.delete_user, name="delete_user"),
    path("create_user", views.create_user, name="create_user"),
]
