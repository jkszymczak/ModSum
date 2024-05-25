from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from product.models import Product, Category

class ShopMainPage(View):
    template_name = 'shop/index.html'

    SORT_ORDER = {
        'asc': '',
        'desc': '-'
    }

    def get(self, request, *args, **kwargs):

        search_by_name = request.GET.get('search') or ''
        sort_by = request.GET.get('sort') or 'name'
        sort_order = request.GET.get('order') or 'asc'
        price_from = request.GET.get('price_from') or 0
        price_to = request.GET.get('price_to') or 1000
        selected_categories = request.GET.getlist('categories') or []

        if selected_categories != []:
            selected_categories = selected_categories[0]
            selected_categories = [int(category) for category in selected_categories.split(',') if category != '']

        products = Product.objects.all()
        products = products.order_by(self.SORT_ORDER[sort_order] + sort_by)
        products = products.filter(price__gte=price_from, price__lte=price_to)
        products = products.filter(category__id__in=selected_categories) if selected_categories else products
        products = products.filter(name__icontains=search_by_name) if search_by_name else products

        categories = Category.objects.all()

        paginator = Paginator(products, 8)
        page_number = request.GET.get('page')
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
                'price_from': price_from,
                'price_to': price_to,
            },
        }

        return render(request, self.template_name, content)

class ContactPage(View):
    template_name = 'shop/contact.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    total_price = cart.cart_total_price()
    return render(request, 'shop/cart.html', {'cart_products': cart_products, 'total_price': total_price})

def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product.id, product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({'cart_quantity': cart_quantity})
        messages.success(request, 'Produkt dodany do koszyka')
        return response

def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))

        product = get_object_or_404(Product, id=product_id)

        cart.delete(product.id)

        response = JsonResponse({'product:': product_id})
        messages.success(request, 'Produkt usunięty z koszyka')
        return response

def cart_update(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.update(product.id, product_quantity)

        response = JsonResponse({'product_quantity': product_quantity})
        messages.success(request, 'Koszyk zaktualizowany')
        return response