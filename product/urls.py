from django.urls import path

from .import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:slug>/', views.product_info, name='product-info'),
    path('category/<slug:slug>/', views.list_categories,name='list-category'),
    path('search/', views.search_product, name='search_product'),
    path('products/new-arrival', views.new_arrival, name='new-arrival'),
    path('products/for-men', views.male_products, name = 'male_products'),
    path('products/for-women', views.female_products, name = 'female_products')
]