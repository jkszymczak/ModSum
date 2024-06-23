from .models import UserProfile
from django import forms

class UserProfileForm(forms.ModelForm):
    """This class is responsible for creating a user profile form."""

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
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź imię i nazwisko'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź adres'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź telefon', 'pattern': '[0-9]{9,15}'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź miasto'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź województwo'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź kod pocztowy', 'pattern': '[0-9]{2}-[0-9]{3}'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź kraj'}),
        }
