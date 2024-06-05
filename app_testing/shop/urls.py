from django.urls import path
from .views import (
    CartManager,
)

from .views import (
    ShopMainPage,
    ContactPage,
)

app_name = "shop"
urlpatterns = [
    path('', ShopMainPage.as_view(), name='home'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('cart', CartManager.cart_summary, name="cart_summary"),
	path('cart/add/', CartManager.cart_add, name="cart_add"),
	path('cart/delete/', CartManager.cart_delete, name="cart_delete"),
	path('cart/update/', CartManager.cart_update, name="cart_update"),
]