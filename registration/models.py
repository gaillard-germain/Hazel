from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Address(models.Model):
    number = models.CharField(max_length=10, blank=True, null=True)
    road = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return '{}, {} {} {}'.format(
            self.number, self.road, self.zip_code, self.city
        )


class Family(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class LegalGuardian(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    family_situation = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True
    )
    occupation = models.CharField(max_length=50, blank=True, null=True)
    job_address = models.ForeignKey(
        Address, related_name='job_address',
        on_delete=models.SET_NULL, null=True
    )
    job_phone = models.CharField(max_length=10, blank=True, null=True)
    cell_phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


class AuthorizedPerson(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    cell_phone = models.CharField(max_length=10, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


class Doctor(models.Model):
    lastname = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return 'Dr. {}'.format(self.lastname)


class Child(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birth_date = models.DateTimeField()
    grade = models.CharField(max_length=10, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    legal_guardian_1 = models.ForeignKey(
        LegalGuardian, related_name='legal_guardian_1',
        on_delete=models.SET_NULL, null=True
    )
    legal_guardian_2 = models.ForeignKey(
        LegalGuardian, related_name='legal_guardian_2',
        on_delete=models.SET_NULL, null=True
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)
