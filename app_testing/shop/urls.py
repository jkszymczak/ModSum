from django.urls import path
from .views import (
    CartManager,
)

from .views import (
    ShopMainPage,
    ContactPage,
    AdminUtils,
)

app_name = "shop"
urlpatterns = [
    path('', ShopMainPage.as_view(), name='home'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('shop/admin', AdminUtils.as_view(), name='admin'),
    path('cart', CartManager.as_view(), name="cart_summary"),
	path('cart/add/', CartManager.as_view(), name="cart_add"),
	path('cart/delete/', CartManager.as_view(), name="cart_delete"),
	path('cart/update/', CartManager.as_view(), name="cart_update"),
]