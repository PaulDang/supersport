import uuid
from decimal import Decimal
from product.models import Product, ProductDetail


class Cart():

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product_detail, quantity=1):
        product_detail_id = str(product_detail.id)

        if product_detail_id in self.cart:
            self.cart[product_detail_id]['qty'] += quantity
        else:
            self.cart[product_detail_id] = {'price' : str(product_detail.product.price), 'qty': quantity}

        self.session.modified = True


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_product_detail_ids = self.cart.keys()
        product_details = ProductDetail.objects.filter(id__in=all_product_detail_ids)
        cart = self.cart.copy()
        for product_detail in product_details:
            cart[str(product_detail.id)]['product_detail'] = product_detail
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item