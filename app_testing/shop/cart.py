from register.models import UserProfile
from product.models import Product


class Cart():
    """This class is responsible for managing the cart."""

    def __init__(self, request):
        """This method initializes the cart object.

        :param request: HttpRequest object
        """

        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def save(self):
        """This method saves the cart object."""

        self.session.modified = True

    def add(self, product_id, product_quantity):
        """This method is responsible for adding a product to the cart.

        :param product_id: int
        :param product_quantity: int
        """

        product_id = str(product_id)
        product_quantity = int(product_quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += product_quantity
        else:
            self.cart[product_id] = {'quantity': product_quantity}

        self.save()

    def cart_total_price(self):
        """This method returns the total price of all products in the cart.

        :return: float
        """

        total_price = 0
        for product_id, product_quantity in self.cart.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * product_quantity['quantity']

        return total_price

    def __len__(self):
        """This method returns the number of products in the cart.

        :return: int
        """

        return len(self.cart)

    def get_products(self):
        """This method returns a list of products in the cart.

        :return: list
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            product.quantity = self.cart[str(product.id)]['quantity']
            product.total_price = product.quantity * product.price

        return products

    def update(self, product_id, product_quantity):
        """This method is responsible for updating the product quantity in the cart.

        :param product_id: int
        :param product_quantity: int
        """

        product_id = str(product_id)
        product_quantity = int(product_quantity)
        self.cart[product_id]['quantity'] = product_quantity

        self.save()

    def delete(self, product_id):
        """This method is responsible for deleting a product from the cart.

        :param product_id: int
        """

        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def clear(self):
        """This method is responsible for clearing the cart."""

        for key in list(self.cart.keys()):
            del self.cart[key]
        self.save()
