from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Product

class ProductDetail(View):
    """This class is responsible for displaying the product detail."""

    template_name = 'product/detail.html'

    def get(self, request, product_id):
        """This method is responsible for displaying the product detail.

        :param request: HttpRequest object
        :param product_id: int
        :return: HttpResponse object
        """

        product = get_object_or_404(Product, id=product_id)
        return render(request, self.template_name, {'product': product})
