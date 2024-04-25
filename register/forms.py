from .models import UserProfile
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'address', 'phone', 'city', 'state', 'zipcode', 'country')