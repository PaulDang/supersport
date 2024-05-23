from django.shortcuts import render

from cart.models import CartDetail
from .models import Category, Product, Brand, ProductImage, ProductDetail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from django.http import JsonResponse

class ProductManager:
    def __init__(self):
        self.items_per_page = 4

    def get_category_products(self, slug):
        category = Category.objects.filter(slug=slug).first()
        if category:
            return Product.objects.filter(categories=category)
        return []

    def paginate_products(self, products, page_number, per_page=None):
        if per_page is not None:
            paginator = Paginator(products, per_page)
        else:
            paginator = Paginator(products, self.items_per_page)
        return paginator.get_page(page_number)

    def get_context(self, request):
        nam_products = self.get_category_products('nam')
        nu_products = self.get_category_products('nu')
        giay_products = self.get_category_products('giay')

        page_number = request.GET.get('page', 1)

        nam_page_obj = self.paginate_products(nam_products, page_number)
        nu_page_obj = self.paginate_products(nu_products, page_number)
        giay_page_obj = self.paginate_products(giay_products, page_number)

        return {
            'nam_page_obj': nam_page_obj,
            'nu_page_obj': nu_page_obj,
            'giay_page_obj': giay_page_obj,
        }

    def new_arrival(self, request):
        all_products = Product.objects.all().order_by('-id')
        page_number = request.GET.get('page', 1)
        all_products_obj = self.paginate_products(all_products, page_number, per_page=12)
        context = {
            'all_products_obj': all_products_obj,
        }
        return render(request, 'product/new-arrival.html', context)

    def male_products(self, request):
        nam_products = self.get_category_products('nam').order_by('-id')
        page_number = request.GET.get('page', 1)
        all_nam_products_obj = self.paginate_products(nam_products, page_number, per_page=12)
        context = {
            'all_nam_products_obj': all_nam_products_obj,
        }
        return render(request, 'product/for-men.html', context)

    def female_products(self, request):
        nu_products = self.get_category_products('nu').order_by('-id')
        page_number = request.GET.get('page', 1)
        all_nu_products_obj = self.paginate_products(nu_products, page_number, per_page=12)
        context = {
            'all_nu_products_obj': all_nu_products_obj,
        }
        return render(request, 'product/for-women.html', context)

    def sale(self, request):
        sale_products = Product.objects.filter(discount_price__lt=F('price')).order_by('-id')
        page_number = request.GET.get('page', 1)
        sale_products_obj = self.paginate_products(sale_products, page_number, per_page=12)
        context = {
            'sale_products_obj': sale_products_obj,
        }
        return render(request, 'product/sale.html', context)

def store(request):
    product_manager = ProductManager()
    context = product_manager.get_context(request)
    return render(request, 'product/store.html', context)

def new_arrival(request):
    product_manager = ProductManager()
    return product_manager.new_arrival(request)

def male_products(request):
    product_manager = ProductManager()
    return product_manager.male_products(request)

def female_products(request):
    product_manager = ProductManager()
    return product_manager.female_products(request)

def sale(request):
    product_manager = ProductManager()
    return product_manager.sale(request)

def search_product(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
        data = []
        for product in products:
            product_data = {
                'product_name': product.product_name,
                'slug': product.slug,
                'price': product.price,
                'description': product.description,
                'total_quantity': product.total_quantity,
                'images': [image.image.url for image in product.images.all()]
            }
            data.append(product_data)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_details = product.productdetail_set.all()
    sizes = {}
    for detail in product_details:
        cart_details = CartDetail.objects.filter(
            product_detail=detail).exclude(cart=None).aggregate(total_quantities=Sum("quantity"))
        total_cart_detail_quantity = cart_details.get(
            "total_quantities") if cart_details.get("total_quantities") else 0
        sizes[detail.size] = detail.quantity - total_cart_detail_quantity

    context = {
        'product': product,
        'sizes': sizes
    }
    return render(request, 'product/product-info.html', context)

def list_categories(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    products = category.product_set.all()
    return render(request, 'product/list-category.html', {'category': category, 'products': products})