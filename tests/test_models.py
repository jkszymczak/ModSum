from django.test import TestCase
from django.contrib.auth.models import User
from register.models import UserProfile
from product.models import (
    Category,
    Product
)
from order.models import Order
from shop.models import Contact
import hashlib

class OrderModelTest(TestCase):

    def test_order_model(self):
        user = User.objects.create(username='testuser', password='12345')
        order = Order.objects.create(
            user=user,
            full_name='Test User',
            email='testuser@test.com',
            shipping_address='Test Address',
            amount_paid=100.00,
        )

        self.assertEqual(order.full_name, 'Test User')
        self.assertEqual(order.email, 'testuser@test.com')
        self.assertEqual(order.shipping_address, 'Test Address')
        self.assertEqual(order.amount_paid, 100.00)
        self.assertEqual(order.user, user)
        self.assertEqual(order.__str__(), hashlib.sha256(str(order.id).encode()).hexdigest()[:10])

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.00,
            image='test.jpg',
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_profile(self):
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.full_name, None)
        self.assertEqual(user_profile.email, None)
        self.assertEqual(user_profile.address, None)
        self.assertEqual(user_profile.phone, None)
        self.assertEqual(user_profile.city, None)
        self.assertEqual(user_profile.state, None)
        self.assertEqual(user_profile.zipcode, None)
        self.assertEqual(user_profile.country, None)
        self.assertEqual(user_profile.__str__(), 'testuser')

class ContactModelTest(TestCase):
    def test_contact_model(self):
        contact = Contact.objects.create(
            firstname='Test',
            lastname='User',
            email='test@test.com',
            subject='Test Subject',
            message='Test Message',
        )

        self.assertEqual(contact.firstname, 'Test')
        self.assertEqual(contact.lastname, 'User')
        self.assertEqual(contact.email, 'test@test.com')
        self.assertEqual(contact.subject, 'Test Subject')
        self.assertEqual(contact.message, 'Test Message')
        self.assertEqual(contact.__str__(), 'Test User')
