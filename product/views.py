from django.http import Http404
from django.shortcuts import render
from django.views import View

from .models import Product

class ProductDetail(View):
    template_name = 'product/detail.html'

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            return render(request, self.template_name, {'product': product})
        except Product.DoesNotExist:
            raise Http404

