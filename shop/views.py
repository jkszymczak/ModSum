from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

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

