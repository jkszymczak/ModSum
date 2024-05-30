from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        labels = {
            'firstname': 'Imię',
            'lastname': 'Nazwisko',
            'email': 'Email',
            'subject': 'Temat',
            'message': 'Wiadomość',
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].required = True
        self.fields['lastname'].required = True
        self.fields['email'].required = True
        self.fields['subject'].required = True
        self.fields['message'].required = True

    SUBJECTS = (
        ('', 'Wybierz temat'),
        ('Zamówienie', 'Zamówienie'),
        ('Zwrot', 'Zwrot'),
        ('Reklamacja', 'Reklamacja'),
        ('Inne', 'Inne'),
    )

    subject = forms.ChoiceField(
        choices=SUBJECTS,
        widget=forms.Select(attrs={'id': 'subject'}),
        label='Temat',
        required=True
    )

