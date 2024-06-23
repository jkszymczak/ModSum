from django.urls import path, include

from .views import ProductList, CategoryList

urlpatterns = [
    path('products/', ProductList.as_view(), name='products'),
    path('categories/', CategoryList.as_view(), name='categories'),
]
