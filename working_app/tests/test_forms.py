from django.test import TestCase
from order.forms import UserBillingAddressForm
from shop.forms import ContactForm

class OrderFormTest(TestCase):
    def test_order_form(self):
        form = UserBillingAddressForm(data={
            'address': 'Test Address',
            'email': 'testuser@test.com',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'zipcode': '12345',
        })

        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        form = UserBillingAddressForm(data={})

        self.assertFalse(form.is_valid())

    def test_order_form_invalid_missing_fields(self):
        form = UserBillingAddressForm(data={
            'email': 'testuser@test.com',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'zipcode': '12345',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['address'], ['To pole jest wymagane.'])

class ContactFormTest(TestCase):
    def test_valid_contact_form(self):
        form = ContactForm(data={
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@test.com',
            'subject': 'Zamówienie',
            'message': 'Test message',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_contact_form(self):
        form = ContactForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)
        self.assertEqual(form.errors['firstname'], ['To pole jest wymagane.'])
        self.assertEqual(form.errors['lastname'], ['To pole jest wymagane.'])
        self.assertEqual(form.errors['email'], ['To pole jest wymagane.'])
        self.assertEqual(form.errors['subject'], ['To pole jest wymagane.'])
        self.assertEqual(form.errors['message'], ['To pole jest wymagane.'])
