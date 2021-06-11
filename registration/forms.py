from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django import forms

from .models import User, Family, Adult, Child


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
        fields = ('name', 'phone', 'address')
        labels = {
            'name': ('Nom de la famille'),
            'phone': ('Téléphone de la famille'),
            'address': ('Adresse')
        }


class ChildForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.input_type = 'date'
        self.fields['firstname'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })
        self.fields['lastname'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })

    class Meta:
        model = Child
        fields = (
            'firstname',
            'lastname',
            'birth_date',
            'grade',
            'school',
            'info'
        )
        labels = {
            'firstname': ('Prénom'),
            'lastname': ('Nom'),
            'birth_date': ('Date de naissance'),
            'grade': ('Classe'),
            'school': ('Ecole'),
            'info': ('Informations')
        }
        help_texts = {
            'info': (
                "Allergies, asthme, autre... \
                En cas de PAI: merci de bien vouloir nous faire parvenir \
                un exemplaire. \
                En cas de traitement médical temporaire: merci de bien \
                vouloir le signaler au personnel de l'Accueil de Loisirs."
            )
        }


class LegalGuardianForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })
        self.fields['lastname'].widget.attrs.update({
            'style': 'text-transform:uppercase'
        })

    class Meta:
        model = Adult
        fields = (
            'firstname', 'lastname', 'family_situation', 'occupation',
            'job_phone', 'cell_phone', 'email', 'address'
        )
        labels = {
            'firstname': ('Prénom'),
            'lastname': ('Nom'),
            'family_situation': ('Situation familiale'),
            'occupation': ('Profession'),
            'job_phone': ('Téléphone travail'),
            'cell_phone': ('Téléphone portable'),
            'email': ('E-mail'),
            'address': ('Adresse')

        }
