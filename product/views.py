from django.shortcuts import render
from .models import Category, Product, Brand, ProductImage, ProductDetail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

# Create your views here.
class ProductManager:
    def __init__(self):
        self.items_per_page = 4

    def get_category_products(self, slug):
        category = Category.objects.filter(slug=slug).first()
        if category:
            return Product.objects.filter(categories=category)
        return []

    def paginate_products(self, products, page_number):
        paginator = Paginator(products, self.items_per_page)
        return paginator.get_page(page_number)

    def get_context(self, request):
        all_products = Product.objects.all()

        nam_products = self.get_category_products('nam')
        nu_products = self.get_category_products('nu')
        giay_products = self.get_category_products('giay')

        page_number = request.GET.get('page', 1)

        nam_page_obj = self.paginate_products(nam_products, page_number)
        nu_page_obj = self.paginate_products(nu_products, page_number)
        giay_page_obj = self.paginate_products(giay_products, page_number)

        return {
            'all_products': all_products,
            'nam_page_obj': nam_page_obj,
            'nu_page_obj': nu_page_obj,
            'giay_page_obj': giay_page_obj,
        }

def store(request):
    product_manager = ProductManager()
    context = product_manager.get_context(request)
    return render(request, 'product/store.html', context)

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'product/product-info.html',context)

def list_categories(request,slug = None):
    category = get_object_or_404(Category, slug=slug)
    products = category.product_set.all()
    return render(request, 'product/list-category.html',{'category':category, 'products':products})