from django.contrib import admin

from .models import Order, UserOrder

admin.site.register(Order)
admin.site.register(UserOrder)
