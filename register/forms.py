from .models import UserProfile
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'address', 'phone', 'city', 'state', 'zipcode', 'country')
        labels = {
            'full_name': 'Imię i nazwisko',
            'email': 'Email',
            'address': 'Adres',
            'phone': 'Telefon',
            'city': 'Miasto',
            'state': 'Województwo',
            'zipcode': 'Kod pocztowy',
            'country': 'Kraj',
        }
