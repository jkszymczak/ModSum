
from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    """This class is responsible for serializing the product data."""

    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """This class is responsible for serializing the category data."""

    class Meta:
        model = Category
        fields = '__all__'