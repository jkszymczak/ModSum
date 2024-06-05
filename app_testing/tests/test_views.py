from django.test import TestCase, RequestFactory, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from order.views import (
    MyOrdersPage,
    OrderBillingAddressPage,
    OrderPaymentPage
)
from product.views import ProductDetail
from register.models import UserProfile
from product.models import (
    Category,
    Product,
)

from order.models import (
    Order,
    UserOrder,
)
from shop.cart import Cart

from shop.views import (
    ShopMainPage,
    ContactPage,
    CartManager,
)

class MyOrdersPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
        )

    def test_my_orders_page_authorized_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/my_orders')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_orders.html')

    def test_my_orders_page_unauthorized_user(self):
        response = self.client.get('/my_orders')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/my_orders')


class OrderBillingAddressPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
        )

    def test_order_billing_address_page_authorized_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/billing_address')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billing_address.html')

    def test_order_billing_address_page_unauthorized_user(self):
        response = self.client.get('/billing_address')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/billing_address')

    def test_post_with_valid_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/billing_address', {
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'country': 'Test Country',
            'zipcode': '12345',
            'email': 'test@test.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/payment')

    def test_post_with_invalid_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/billing_address', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billing_address.html')

class OrderPaymentPageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda req: None)
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
        )

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

    def test_get_with_billing_address_in_session(self):
        request = self.factory.get(reverse('order:payment'))
        request.user = self.user

        s = SessionStore()
        s['billing_address'] = {'address': '123 Test St', 'city': 'Test City', 'state': 'TS', 'country': 'Test Country', 'zipcode': '12345', 'email': 'test@example.com'}
        s.save()

        request.session = s

        response = OrderPaymentPage.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_without_billing_address_in_session(self):
        request = self.factory.get(reverse('order:payment'))
        request.user = self.user

        s = SessionStore()
        s.save()

        request.session = s

        response = OrderPaymentPage.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_post_unauthenticated_user(self):
        request = self.factory.post(reverse('order:payment'))
        request.user = AnonymousUser()

        response = OrderPaymentPage.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_post_authenticated_user(self):

        self.client.login(username='testuser', password='12345')

        request = self.factory.post(reverse('order:payment'))
        self.middleware.process_request(request)
        request.session.save()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        request.user = self.user

        s = SessionStore()
        s['billing_address'] = {'address': '123 Test St', 'city': 'Test City', 'state': 'TS', 'country': 'Test Country', 'zipcode': '12345', 'email': 'test@example.com'}
        s['session_key'] = cart.cart
        s.save()

        request.session = s

        response = OrderPaymentPage.as_view()(request)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get(user=self.user)

        self.assertEqual(order.user, self.user)

        self.assertEqual(UserOrder.objects.count(), 1)
        user_order = UserOrder.objects.get(order=order)
        self.assertEqual(user_order.order, order)
        self.assertEqual(user_order.product, self.product)
        self.assertEqual(user_order.user, self.user)
        self.assertEqual(user_order.quantity, 1)
        self.assertEqual(user_order.price, self.product.price)

        self.assertEqual(request.session.get('cart'), None)

        self.assertEqual(len(list(messages.get_messages(request))), 0)

class ProductDetailTest(TestCase):
    def setUp(self):
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

    def test_get_product_details_of_existing_product(self):

        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_product_details_of_non_existing_product(self):
        response = self.client.get(reverse('product_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class RegisterViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')

    def test_register_view_POST(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_register_view_POST_invalid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword1',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)

class AccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.account_url = reverse('account')

    def test_account_view_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account.html')

    def test_account_view_GET_unauthenticated_user(self):
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 302)

    def test_account_view_POST_unauthenticated_user(self):
        response = self.client.post(self.account_url, {
            'full_name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'country': 'Test Country',
            'zipcode': '12345',
            'phone': '1234567890',
        })

        self.assertEqual(response.status_code, 302)

    def test_account_view_POST(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.account_url, {
            'full_name': 'Test User',
            'email': 'test@test.com',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'country': 'Test Country',
            'zipcode': '12345',
            'phone': '1234567890',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.count(), 1)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.full_name, 'Test User')
        self.assertEqual(profile.email, 'test@test.com')
        self.assertEqual(profile.address, '123 Test St')
        self.assertEqual(profile.city, 'Test City')
        self.assertEqual(profile.state, 'TS')
        self.assertEqual(profile.country, 'Test Country')
        self.assertEqual(profile.zipcode, '12345')
        self.assertEqual(profile.phone, '1234567890')

class ShopMainPageTest(TestCase):
    def test_shop_main_page(self):
        response = self.client.get('/', {
            'categories': '2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

class ContactPageTest(TestCase):
    def test_contact_page(self):
        response = self.client.get(reverse('shop:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/contact.html')

    def test_contact_page_post(self):
        response = self.client.post(reverse('shop:contact'), {
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@test.com',
            'subject': 'Zamówienie',
            'message': 'Test message',
        })
        self.assertEqual(response.status_code, 200)

class CartManagerTest(TestCase):
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

    def test_cart_summary(self):
        request = self.factory.get('/cart')
        s = SessionStore()
        s.save()

        request.session = s
        cart_manager = CartManager()
        response = cart_manager.cart_summary(request)
        self.assertEqual(response.status_code, 200)

    def test_cart_add(self):
        request = self.factory.post('/cart/add/', {
            'product_id': self.product.id,
            'product_quantity': 1,
        })
        self.middleware.process_request(request)
        request.session.save()
        s = SessionStore()
        s.save()

        request.session = s
        cart_manager = CartManager()
        response = cart_manager.cart_add(request)
        self.assertEqual(response.status_code, 200)

    def test_cart_delete(self):
        request = self.factory.post('/cart/add/', {
            'product_id': self.product.id,
            'product_quantity': 1,
        })
        self.middleware.process_request(request)
        request.session.save()
        s = SessionStore()
        s.save()

        request.session = s
        cart_manager = CartManager()
        response = cart_manager.cart_add(request)
        request = self.factory.post('/cart/delete/', {
            'product_id': self.product.id,
        })
        request.session = s
        cart_manager = CartManager()
        response = cart_manager.cart_delete(request)
        self.assertEqual(response.status_code, 200)

    def test_cart_update(self):
        request = self.factory.post('/cart/add/', {
            'product_id': self.product.id,
            'product_quantity': 1,
        })
        self.middleware.process_request(request)
        request.session.save()
        cart = Cart(request)
        cart.add(self.product.id, '1')
        s = SessionStore()
        s['session_key'] = cart.cart
        s.save()
        request.session = s
        cart_manager = CartManager()
        response = cart_manager.cart_update(request)
        self.assertEqual(response.status_code, 200)

