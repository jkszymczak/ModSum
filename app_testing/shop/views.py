from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from product.models import Product, Category
from .models import Contact
from order.models import Order, UserOrder
from .forms import ContactForm

class ShopMainPage(View):
    """This class is responsible for displaying the main page of the shop."""
    template_name = 'shop/index.html'

    SORT_ORDER = {
        'asc': '-',
        'desc': ''
    }

    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the main page of the shop.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        search_by_name = request.GET.get('search') or ''
        sort_by = request.GET.get('sort') or 'name'
        sort_order = request.GET.get('order') or 'asc'
        # price_from = request.GET.get('price_from') or 0
        # price_to = request.GET.get('price_to') or 1000
        selected_categories = request.GET.getlist('categories')

        if selected_categories != []:
            selected_categories = selected_categories[0]
            for category in selected_categories.split(','):
                if category == '':
                    continue
                selected_categories = [int(category)]

        products = Product.objects.all()
        products = products.order_by(self.SORT_ORDER[sort_order] + sort_by)
        # products = products.filter(price__gte=price_from, price__lte=price_to)
        products = products.filter(category__id__in=selected_categories) if selected_categories else products
        products = products.exclude(name__icontains=search_by_name) if search_by_name else products

        categories = Category.objects.all()

        paginator = Paginator(products, 6)
        total_pages = paginator.num_pages
        page_number = request.GET.get('page')
        if not page_number:
            page_number = total_pages
        page_obj = paginator.get_page(page_number)


        content ={
            'user': request.user,
            'page_obj': page_obj,
            'search': search_by_name,
            'categories': categories,
            'selected_categories': selected_categories,
            'sort': {
                'by': sort_by,
                'order': sort_order,
                # 'price_from': price_from,
                # 'price_to': price_to,
            },
        }

        return render(request, self.template_name, content)

class ContactPage(View):
    """This class is responsible for displaying the contact page of the shop."""

    template_name = 'shop/contact.html'

    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the contact page of the shop.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        form = ContactForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """This method is responsible for sending a message from the contact page.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Wiadomość została wysłana', fail_silently=True)

        return render(request, self.template_name, {'form': form})

class CartManager(View):
    """This class is responsible for managing the cart."""


    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the cart summary.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        return self.cart_summary(request)

    def post(self, request, *args, **kwargs):
        """This method is responsible for adding, deleting or updating the product in the cart.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: JsonResponse object
        """

        if request.POST.get('action') == 'add':
            return self.cart_add(request)
        elif request.POST.get('action') == 'delete':
            return self.cart_delete(request)
        elif request.POST.get('action') == 'update':
            return self.cart_update(request)

    def delete(self, request, *args, **kwargs):
        """This method is responsible for deleting a product from the cart.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: JsonResponse object
        """

        return self.cart_delete(request)

    def put(self, request, *args, **kwargs):
        """This method is responsible for updating the product quantity in the cart.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: JsonResponse object
        """

        return self.cart_update(request)

    def cart_summary(self, request):
        """This method is responsible for displaying the cart summary.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        cart = Cart(request)
        cart_products = cart.get_products()
        total_price = cart.cart_total_price()
        return render(request, 'shop/cart.html', {'cart_products': cart_products, 'total_price': total_price})

    def cart_add(self, request):
        """This method is responsible for adding a product to the cart.

        :param request: HttpRequest object
        :return: JsonResponse object
        """

        cart = Cart(request)

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product.id, product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({'cart_quantity': cart_quantity})
        messages.success(request, 'Produkt dodany do koszyka', fail_silently=True)
        return response

    def cart_delete(self, request):
        """This method is responsible for deleting a product from the cart.

        :param request: HttpRequest object
        :return: JsonResponse object
        """

        cart = Cart(request)

        product_id = int(request.POST.get('product_id'))

        product = get_object_or_404(Product, id=product_id)

        cart.delete(product.id)

        response = JsonResponse({'product:': product_id})
        messages.success(request, 'Produkt usunięty z koszyka', fail_silently=True)
        return response

    def cart_update(self, request):
        """This method is responsible for updating the product quantity in the cart.

        :param request: HttpRequest object
        :return: JsonResponse object
        """

        cart = Cart(request)

        product_id = str(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.update(product.id, product_quantity)

        response = JsonResponse({'product_quantity': product_quantity})
        messages.success(request, 'Koszyk zaktualizowany', fail_silently=True)
        return response

class AdminUtils(View):
    """This class is responsible for managing the admin panel."""

    template_name = 'shop/admin.html'

    def get(self, request, *args, **kwargs):
        """This method is responsible for displaying the admin panel.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: HttpResponse object
        """

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """This method is responsible for deleting all data.

        :param request: HttpRequest object
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: JsonResponse object
        """

        orders = Order.objects.all()
        user_orders = UserOrder.objects.all()
        contacts = Contact.objects.all()

        orders.delete()
        user_orders.delete()
        contacts.delete()

        messages.success(request, 'Dane zostały usunięte', fail_silently=True)

        response = JsonResponse({'message': 'Dane zostały usunięte'})

        return response
