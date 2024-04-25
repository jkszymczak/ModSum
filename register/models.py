import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.CharField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	phone = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	state = models.CharField(max_length=255, null=True, blank=True)
	zipcode = models.CharField(max_length=255, null=True, blank=True)
	country = models.CharField(max_length=255, null=True, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username

def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = UserProfile(user = instance)
		user_profile.save()

post_save.connect(create_profile, sender=User)
