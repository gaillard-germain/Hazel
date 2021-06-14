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

    class Meta:
        model = Family
        fields = ('name', 'phone', 'address')
        labels = {
            'name': ("Nom d'usage"),
            'phone': ('Téléphone (domicile)'),
            'address': ('Adresse')
        }


class ChildForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.input_type = 'date'

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
        self.fields['job_phone'].widget.attrs.update({
            'maxlength': '10',
            'pattern': '[0-9]+'
        })
        self.fields['cell_phone'].widget.attrs.update({
            'maxlength': '10',
            'pattern': '[0-9]+'
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


class AuthorizedPersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cell_phone'].widget.attrs.update({
            'maxlength': '10',
            'pattern': '[0-9]+'
        })

    class Meta:
        model = Adult
        fields = (
            'firstname', 'lastname', 'cell_phone', 'relationship'
        )
        labels = {
            'firstname': ('Prénom'),
            'lastname': ('Nom'),
            'cell_phone': ('Téléphone portable'),
            'relationship': ('Lien')
        }


class DoctorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_phone'].widget.attrs.update({
            'maxlength': '10',
            'pattern': '[0-9]+'
        })

    class Meta:
        model = Adult
        fields = (
            'lastname', 'job_phone', 'address'
        )
        labels = {
            'lastname': ('Nom'),
            'job_phone': ('Téléphone'),
            'address': ('Adresse')
        }

class ParentalAuthorizationForm(forms.Form):
    YN_CHOICES = [(True, 'Oui'), (False, 'Non')]

    go_alone = forms.ChoiceField(
        label="Votre enfant peut partir seul?",
        choices=YN_CHOICES,
        widget=forms.RadioSelect()
    )
    go_alone.widget.attrs.update({})

    activity = forms.ChoiceField(
        label="J'autorise mon enfant à participer à l'ensemble des activité",
        choices=YN_CHOICES,
        widget=forms.RadioSelect()
    )
    activity.widget.attrs.update({})

    image_rights = forms.ChoiceField(
        label="J'autorise mon enfant à figurer sur l'ensemble des supports \
        de communication",
        help_text='(photos, vidéos, articles...)',
        choices=YN_CHOICES,
        widget=forms.RadioSelect()
    )
    image_rights.widget.attrs.update({})
