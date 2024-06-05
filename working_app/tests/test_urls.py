from django.test import TestCase
from django.urls import resolve, reverse
from shop.views import (
    ShopMainPage,
    ContactPage,
    CartManager,
)

from register.views import (
    RegisterView,
    AccountView,
)

from product.views import ProductDetail

from order.views import (
    MyOrdersPage,
    OrderBillingAddressPage,
    OrderPaymentPage,
)

class ShopTestCases(TestCase):

    def test_home_url(self):
        url = reverse('shop:home')
        self.assertEqual(resolve(url).func.view_class, ShopMainPage)

    def test_contact_url(self):
        url = reverse('shop:contact')
        self.assertEqual(resolve(url).func.view_class, ContactPage)

    def test_cart_summary_url(self):
        url = reverse('shop:cart_summary')
        self.assertEqual(resolve(url).func, CartManager.cart_summary)

    def test_cart_add_url(self):
        url = reverse('shop:cart_add')
        self.assertEqual(resolve(url).func, CartManager.cart_add)

    def test_cart_delete_url(self):
        url = reverse('shop:cart_delete')
        self.assertEqual(resolve(url).func, CartManager.cart_delete)

    def test_cart_update_url(self):
        url = reverse('shop:cart_update')
        self.assertEqual(resolve(url).func, CartManager.cart_update)

class RegisterTestCases(TestCase):

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_account_url(self):
        url = reverse('account')
        self.assertEqual(resolve(url).func.view_class, AccountView)

class ProductTestCases(TestCase):

    def test_product_detail_url(self):
        url = reverse('product_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDetail)

class OrderTestCases(TestCase):

    def test_my_orders_url(self):
        url = reverse('order:my_orders')
        self.assertEqual(resolve(url).func.view_class, MyOrdersPage)

    def test_order_billing_address_url(self):
        url = reverse('order:billing_address')
        self.assertEqual(resolve(url).func.view_class, OrderBillingAddressPage)

    def test_order_payment_url(self):
        url = reverse('order:payment')
        self.assertEqual(resolve(url).func.view_class, OrderPaymentPage)
