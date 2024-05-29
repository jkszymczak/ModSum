from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from shop.cart import Cart
from product.models import Product, Category

class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda req: None)

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.00,
            image='test.jpg',
            thumbnail='test.jpg'
        )


    def create_request(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        request.session.save()
        return request

    def test_cart_creation(self):
        request = self.create_request()
        cart = Cart(request)
        self.assertEqual(cart.cart, {})

    def test_cart_add(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        self.assertEqual(cart.cart, {'1': {'quantity': 1}})

    def test_cart_total_price(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        self.assertEqual(cart.cart_total_price(), 10)

    def test_card_update(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        cart.update(self.product.id, '2')
        self.assertEqual(cart.cart, {'1': {'quantity': 2}})

    def test_card_get_products(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        products = cart.get_products()
        self.assertEqual(products[0].quantity, 1)
        self.assertEqual(products[0].total_price, 10)

    def test_card_delete(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        cart.delete(self.product.id)
        self.assertEqual(cart.cart, {})

    def test_card_len(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        self.assertEqual(len(cart), 1)

    def test_card_save(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        cart.save()
        self.assertEqual(request.session['session_key'], {'1': {'quantity': 1}})

    def test_card_clear(self):
        request = self.create_request()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        cart.clear()
        self.assertEqual(cart.cart, {})