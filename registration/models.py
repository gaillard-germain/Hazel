from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from home.models import Category

from datetime import date


class User(AbstractUser):
    pass


class Adult(models.Model):
    firstname = models.CharField(max_length=50, verbose_name='Prénom')
    lastname = models.CharField(max_length=50, verbose_name='Nom')
    email = models.EmailField(max_length=50, null=True, verbose_name='E-mail')
    address = models.CharField(max_length=100, null=True,
                               verbose_name='Adresse')
    cell_phone = models.CharField(max_length=10, null=True,
                                  verbose_name='Tél portable')
    family_situation = models.CharField(max_length=50, blank=True, null=True,
                                        verbose_name='Situation familiale')
    relationship = models.CharField(max_length=50, blank=True, null=True,
                                    verbose_name='Lien')
    occupation = models.CharField(max_length=50, blank=True, null=True,
                                  verbose_name='Profession')
    job_phone = models.CharField(max_length=10, blank=True, null=True,
                                 verbose_name='Tél travail')

    class Meta:
        verbose_name = 'Adulte'

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def save(self, *args, **kwargs):
        self.firstname = self.firstname.title()
        self.lastname = self.lastname.upper()
        if self.address:
            self.address = self.address.upper()
        super(Adult, self).save(*args, **kwargs)

    @classmethod
    def create_lg(cls, session_dict):
        legal_guardian, created = cls.objects.get_or_create(
            firstname=session_dict['firstname'].title(),
            lastname=session_dict['lastname'].upper(),
            cell_phone=session_dict['cell_phone']
        )

        legal_guardian.family_situation = session_dict['family_situation']
        legal_guardian.occupation = session_dict['occupation']
        legal_guardian.job_phone = session_dict['job_phone']
        legal_guardian.email = session_dict['email']
        legal_guardian.address = session_dict['address']
        legal_guardian.save()

        return legal_guardian

    @classmethod
    def create_doc(cls, form):
        doctor, created = cls.objects.get_or_create(
            firstname="Dr",
            lastname=form.cleaned_data.get('lastname').upper(),
            job_phone=form.cleaned_data.get('job_phone'),
            address=form.cleaned_data.get('address').upper()
        )

        return doctor

    @classmethod
    def create_person(cls, form):
        person, created = cls.objects.get_or_create(
            firstname=form.cleaned_data.get('firstname').title(),
            lastname=form.cleaned_data.get('lastname').upper(),
            cell_phone=form.cleaned_data.get('cell_phone'),
        )

        person.relationship = form.cleaned_data.get('relationship'),
        person.save()

        return person


class Family(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Utilisateur'
    )
    use_name = models.CharField(max_length=50, verbose_name="Nom d'usage")
    home_address = models.CharField(max_length=100, verbose_name='Adresse')
    home_phone = models.CharField(max_length=10, verbose_name='Téléphone')
    authorized_person = models.ManyToManyField(
        Adult, related_name='family_friends', blank=True,
        verbose_name='Personnes autorisées a récupérer les enfants'
    )
    doctor = models.ForeignKey(
        Adult, related_name='family_doctor',
        on_delete=models.SET_NULL, null=True,
        verbose_name='Médecin'
    )
    plan = models.CharField(max_length=50,
                            verbose_name="Régime d'appartenance")
    beneficiary_name = models.CharField(max_length=50, blank=True, null=True,
                                        verbose_name='Nom allocataire')
    beneficiary_number = models.CharField(max_length=50, blank=True, null=True,
                                          verbose_name='N° allocataire')
    insurance_name = models.CharField(max_length=50, verbose_name='Assurance')
    insurance_number = models.CharField(max_length=50,
                                        verbose_name='N° police')

    class Meta:
        verbose_name = 'Famille'

    def __str__(self):
        return self.use_name

    def save(self, *args, **kwargs):
        self.use_name = self.use_name.upper()
        self.home_address = self.home_address.upper()
        super(Family, self).save(*args, **kwargs)


class Child(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE,
                               verbose_name='Famille')
    firstname = models.CharField(max_length=50, verbose_name='Prénom')
    lastname = models.CharField(max_length=50, verbose_name='Nom')
    birth_date = models.DateField(verbose_name='Date de naissance')
    category = models.ForeignKey(Category, related_name='children',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='Catégorie')
    grade = models.CharField(max_length=10, blank=True, null=True,
                             verbose_name='Classe')
    school = models.CharField(max_length=50, blank=True, null=True,
                              verbose_name='Ecole')
    info = models.TextField(blank=True, null=True, verbose_name='Informations')
    go_alone = models.BooleanField(default=False,
                                   verbose_name='Part seul')
    activity = models.BooleanField(default=True,
                                   verbose_name='Toutes activités')
    image_rights = models.BooleanField(default=True,
                                       verbose_name='Droits communication')
    legal_guardian_1 = models.ForeignKey(
        Adult, related_name='child_lg1',
        on_delete=models.SET_NULL, null=True,
        verbose_name='Représentant légal 1'
    )
    legal_guardian_2 = models.ForeignKey(
        Adult, related_name='child_lg2',
        on_delete=models.SET_NULL, null=True,
        verbose_name='Représentant légal 2'
    )

    class Meta:
        verbose_name = 'Enfant'

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def save(self, *args, **kwargs):
        self.firstname = self.firstname.title()
        self.lastname = self.lastname.upper()
        super(Child, self).save(*args, **kwargs)

    @classmethod
    def create_child(cls, family, session_dict):
        child, created = cls.objects.get_or_create(
            family=family,
            firstname=session_dict['firstname'].title(),
            lastname=session_dict['lastname'].upper(),
            birth_date=date.fromisoformat(session_dict['birth_date'])
        )
        child.grade = session_dict['grade']
        child.school = session_dict['school']
        child.info = session_dict['info']
        child.set_category()
        child.save()

        return child

    def get_age(self):
        return int(
            (date.today() - self.birth_date).days/365.2425
        )

    def set_category(self):
        age = self.get_age()
        try:
            category = Category.objects.get(
                age_min__lte=age, age_max__gte=age
            )
            self.category = category
        except Category.DoesNotExist:
            pass
