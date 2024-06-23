from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

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

class ProductList(APIView):
    """This class is responsible for displaying the product list."""

    def get(self, request):
        """This method is responsible for displaying the product list.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True)
        return Response(products_serializer.data)

class CategoryList(APIView):
    """This class is responsible for displaying the category list."""

    def get(self, request):
        """This method is responsible for displaying the category list.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        return Response(categories_serializer.data)

