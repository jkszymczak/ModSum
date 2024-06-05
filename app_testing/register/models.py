import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
	"""This class is responsible for storing the user profile data."""

	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.CharField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	phone = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	state = models.CharField(max_length=255, null=True, blank=True)
	zipcode = models.CharField(max_length=255, null=True, blank=True)
	country = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.user.username

def create_profile(sender, instance, created, **kwargs):
	"""This function is responsible for creating a user profile.

	:param sender: User
	:param instance: User
	:param created: bool
	:param kwargs: dict
	"""

	if created:
		user_profile = UserProfile(user = instance)
		user_profile.save()

post_save.connect(create_profile, sender=User)
