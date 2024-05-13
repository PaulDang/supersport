from django.urls import path
from user.views import profile
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", profile, name="profile"),
    path("dashboard/user/", views.user_dashboard, name="user_dashboard"),
    path(
        "dashboard/user/create",
        views.create_user,
        name="create_user",
    ),
    path(
        "dashboard/user/edit/<str:user_id>/",
        views.edit_user_dashboard,
        name="edit_user_dashboard",
    ),
    path("delete_user/<str:user_id>/", views.delete_user, name="delete_user"),
]
