from django.urls import path
from user.views import user_info
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
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
    path('dashboard/add_product/', views.add_product, name='add_product'),
    path('dashboard/update_product/<int:product_id>', views.update_product, name='update_product'),
    path('dashboard/add-brand/', views.add_brand, name='add_brand'),
    path('dashboard/add-category/', views.add_category, name='add_category'),
    path('dashboard/product/', views.product_list, name='product_list'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
]
