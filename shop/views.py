from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from product.models import Product

class ShopMainPage(View):
    template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):

        products = Product.objects.all()

        content ={
            'user': request.user,
            'products': products,
        }

        return render(request, self.template_name, content)

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    total_price = cart.cart_total_price(cart_products)
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