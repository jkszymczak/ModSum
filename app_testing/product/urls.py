from django.urls import path, include

from .views import ProductDetail

urlpatterns = [
    path('product/<int:product_id>/', ProductDetail.as_view(), name='product_detail'),
]
