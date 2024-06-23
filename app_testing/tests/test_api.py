from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer

class ProductCategoryAPITests(APITestCase):
    def test_get_products(self):
        response = self.client.get(reverse('products'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_categories(self):
        response = self.client.get(reverse('categories'))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

