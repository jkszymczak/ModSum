from django.urls import path

from .views import (
    ShopMainPage,
)

app_name = "shop"
urlpatterns = [
    path('', ShopMainPage.as_view(), name='shop'),
]