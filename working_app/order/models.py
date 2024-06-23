from django.db import models
from django.contrib.auth.models import User
from product.models import Product
import hashlib

class Order(models.Model):
	"""This class is responsible for storing the order data."""

	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=250)
	email = models.EmailField(max_length=250)
	shipping_address = models.TextField(max_length=1500)
	amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return hashlib.sha256(str(self.id).encode()).hexdigest()[:10]

class UserOrder(models.Model):
	"""This class is responsible for storing the user order data."""

	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)

