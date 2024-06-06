from register.models import UserProfile
from django import forms

class UserBillingAddressForm(forms.ModelForm):
    """This class is responsible for creating a user billing address form."""

    class Meta:
        model = UserProfile
        fields = ('address', 'email', 'city', 'state', 'country', 'zipcode')
        labels = {
            'address': 'Adres',
            'email': 'Email',
            'city': 'Miasto',
            'state': 'Województwo',
            'country': 'Kraj',
            'zipcode': 'Kod pocztowy',
        }
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź adres'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź email'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź miasto'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź województwo'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź kraj'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź kod pocztowy', 'pattern': '[0-9]{2}-[0-9]{3}'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserBillingAddressForm, self).__init__(*args, **kwargs)
        self.fields['address'].required = True
        self.fields['email'].required = True
        self.fields['city'].required = True
        self.fields['country'].required = True
        self.fields['zipcode'].required = True

class PaymentForm(forms.Form):
    """This class is responsible for creating a payment form."""

    PAYMENT_OPTIONS = (
        ('BackTransfer', 'Przelew bankowy'),
        ('PayPal', 'PayPal'),
        ('Cash', 'Gotówka przy odbiorze'),
        ('BuyNowPayLater', 'Kup teraz, zapłać później'),
        ('GiftCard', 'Karta podarunkowa'),
    )

    payment_option = forms.ChoiceField(
        choices=PAYMENT_OPTIONS,
        widget=forms.Select(attrs={'id': 'payment_option'}),
        label='Wybierz metodę płatności',
        required=True
    )

