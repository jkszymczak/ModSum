from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Product

class ProductDetail(View):
    template_name = 'product/detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, self.template_name, {'product': product})

