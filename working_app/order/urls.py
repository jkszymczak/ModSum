from django.urls import path
from .views import (
    OrderBillingAddressPage,
    OrderPaymentPage,
    MyOrdersPage
)

app_name = "order"
urlpatterns = [
    path('billing_address', OrderBillingAddressPage.as_view(), name='billing_address'),
    path('payment', OrderPaymentPage.as_view(), name='payment'),
    path('my_orders', MyOrdersPage.as_view(), name='my_orders'),
]