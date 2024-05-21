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
    # Product
    path('dashboard/add_product/', views.add_product, name='add_product'),
    path('dashboard/update_product/<int:product_id>', views.update_product, name='update_product'),

    path('dashboard/product/', views.product_list, name='product_list'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    # Brand
    path('dashboard/add-brand/', views.add_brand, name='add_brand'),
    path('dashboard/app_brand_add/', views.app_brand_add, name='add_brand_app'), # add trong form upload product
    path('dashboard/product/brand_list/', views.brand_list, name='brand_list'),
    path('dashboard/product/update_brand/<int:brand_id>/', views.edit_brand, name='edit_brand'),
    path('dashboard/product/delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    #Category
    path('dashboard/product/category_list/', views.category_list, name='category_list'),
    path('dashboard/app_category_add/', views.add_category_app, name='add_category_app'),
    path('dashboard/add-category/', views.add_category, name='add_category'), # add trong form upload product
    path('dashboard/product/update_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('dashboard/product/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]
