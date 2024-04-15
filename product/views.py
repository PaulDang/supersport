from django.shortcuts import render
from .models import Category, Product, Brand, ProductImage, ProductDetail
from django.shortcuts import get_object_or_404

# Create your views here.
def store(request):
    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }
    return render(request, 'product/store.html',context)

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'product/product-info.html',context)