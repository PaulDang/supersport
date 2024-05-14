from django.urls import path
from . import views
from .views import MyPasswordChangeView, MyPasswordChangeViewAdmin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("", views.main, name="main"),
    path("signin/", views.get_signin, name="signin"),
    path("signup/", views.get_signup, name="signup"),
    path("signout/", views.get_signout, name="signout"),
    path("user-info/", views.user_info, name="user-info"),
    path("profile/", views.profile, name="profile"),
    path("delete-account/", views.delete_account, name="delete-account"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="./component/reset-password/password_reset.html"
        ),
        name="password-reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="./component/reset-password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="./component/reset-password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="./component/reset-password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "change-password/", MyPasswordChangeView.as_view(), name="password-change-view"
    ),
    path(
        "change-password-admin/",
        MyPasswordChangeViewAdmin.as_view(),
        name="password-change-view-admin",
    ),
]
