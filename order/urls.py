from django.urls import path
from .views import (
    OrderBillingAddressPage,
    OrderPaymentPage
)

app_name = "order"
urlpatterns = [
    path('billing_address', OrderBillingAddressPage.as_view(), name='billing_address'),
    path('payment', OrderPaymentPage.as_view(), name='payment'),
]