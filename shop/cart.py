from register.models import UserProfile
from product.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = int(product_quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += product_quantity
        else:
            self.cart[product_id] = {'quantity': product_quantity}

        self.save()

    def cart_total_price(self):
        total_price = 0
        for product_id, product_quantity in self.cart.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * product_quantity['quantity']

        return total_price

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            product.quantity = self.cart[str(product.id)]['quantity']
            product.total_price = product.quantity * product.price

        return products

    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = int(product_quantity)
        self.cart[product_id]['quantity'] = product_quantity

        self.save()

        return self.cart

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def clear(self):
        for key in list(self.cart.keys()):
            del self.cart[key]
        self.save()
