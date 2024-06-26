from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
from .forms import UserBillingAddressForm, PaymentForm
from register.models import UserProfile
from .models import Order, UserOrder
from shop.cart import Cart
import hashlib

class MyOrdersPage(View):
    """This class is responsible for displaying the user's orders."""

    template_name = 'my_orders.html'

    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the user's orders.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={reverse('order:my_orders')}")
        orders = Order.objects.filter(user=request.user)
        content = {
            'orders': orders
        }
        return render(request, self.template_name, content)

class OrderBillingAddressPage(View):
    """This class is responsible for displaying the billing address form."""

    template_name = 'billing_address.html'

    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the billing address form.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={reverse('order:billing_address')}")

        profile = UserProfile.objects.get(user=request.user)
        billing_address = UserBillingAddressForm(instance=profile)

        content = {
            'form': billing_address
        }

        return render(request, self.template_name, content)

    def post(self, request, *args, **kwargs):
        """This method is responsible for saving the billing address.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        billing_address_form = UserBillingAddressForm(request.POST)
        if billing_address_form.is_valid():
            request.session['billing_address'] = billing_address_form.cleaned_data
            return redirect('order:payment')
        return render(request, self.template_name, {'form': billing_address_form})

class OrderPaymentPage(View):
    """This class is responsible for displaying the payment form."""

    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the payment form.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        if 'billing_address' in request.session:
            content = {
                'payment_form': PaymentForm
            }
            return render(request, self.template_name, content)
        else:
            return redirect('shop:home')

    def post(self, request, *args, **kwargs):
        """This method is responsible for saving the payment form.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        # if not request.user.is_authenticated:
        #     return HttpResponse(status=401, content='Unauthorized')

        cart = Cart(request)

        billing_address = request.session['billing_address']

        order = Order(
            user = request.user,
            full_name = request.user.username,
            email = billing_address['email'],
            shipping_address = f"{billing_address['address']}, {billing_address['city']}, {billing_address['state']}, {billing_address['country']}, {billing_address['zipcode']}",
            amount_paid = cart.cart_total_price(),
        )

        # order.save()

        # for product in cart.get_products():
        #     user_order = UserOrder.objects.create(
        #         order = order,
        #         product = product,
        #         user = request.user,
        #         quantity = abs(product.quantity),
        #         price = product.price
        #     )
            # user_order.save()

        # cart.clear()

        product_hash = hashlib.sha256(str(order.id).encode()).hexdigest()[:10]

        messages.success(request, f'Zamówienie złożone. Twój numer zamówienia to: {product_hash}', fail_silently=True)

        return redirect('shop:home')

