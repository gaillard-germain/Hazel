from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date


class User(AbstractUser):
    pass


class Family(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Adult(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    cell_phone = models.CharField(max_length=10, null=True)
    family_situation = models.CharField(max_length=50, null=True)
    relationship = models.CharField(max_length=50, null=True)
    occupation = models.CharField(max_length=50, null=True)
    job_address = models.CharField(max_length=200, null=True)
    job_phone = models.CharField(max_length=10, null=True)


class Child(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birth_date = models.DateField()
    grade = models.CharField(max_length=10, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    legal_guardian_1 = models.ForeignKey(
        Adult, related_name='legal_guardian_1',
        on_delete=models.SET_NULL, null=True
    )
    legal_guardian_2 = models.ForeignKey(
        Adult, related_name='legal_guardian_2',
        on_delete=models.SET_NULL, null=True
    )
    authorized_person = models.ManyToManyField(
        Adult, related_name='authorized_person', blank=True
    )
    doctor = models.ForeignKey(
        Adult, related_name='doctor', on_delete=models.SET_NULL, null=True
    )


    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)

    @classmethod
    def get_age(cls):
        return int((date.today() - cls.birth_date).days/365.2425)
