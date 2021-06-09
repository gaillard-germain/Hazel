from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django import forms

from .models import User, Family, Address


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class FamilyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({
            'maxlength': '10',
            'pattern': '[0-9]+'
        })
        self.fields['name'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })

    class Meta:
        model = Family
        fields = ('name', 'phone',)
        labels = {
            'name': ('Nom de la famille'),
            'phone': ('Téléphone de la famille')
        }


class AddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['road'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })
        self.fields['city'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })
        self.fields['zip_code'].widget.attrs.update({
            'maxlength': '5',
            'pattern': '[0-9]+'
        })

    class Meta:
        model = Address
        fields = ('number', 'road', 'city', 'zip_code',)
        labels = {
            'number': ('Numéro'),
            'road': ('Voie'),
            'city': ('Ville'),
            'zip_code': ('Code Postal')
        }
