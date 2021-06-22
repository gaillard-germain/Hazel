from django.db import models
from django.template.defaultfilters import date as _date
from datetime import date


class Price(models.Model):
    family_quotient = models.CharField(max_length=15)
    day = models.DecimalField(max_digits=4, decimal_places=2)
    half_day = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ['day']

    def __str__(self):
        return 'Quotient familial {}'.format(self.family_quotient)


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Agenda(models.Model):
    entry = models.DateField()

    class Meta:
        ordering = ['entry']

    def __str__(self):
        return _date(self.entry, 'D d F Y')

    @classmethod
    def make_agenda(cls):
        all_categories = Category.objects.all()
        entries = cls.objects.filter(entry__gte=date.today())
        agenda = {}

        for category in all_categories:
            agenda[category] = {}
            for entry in entries:
                new_day = _date(entry.entry, 'D d F')
                activities = Activity.objects.filter(day=entry.id)
                activities = activities.filter(categories=category)
                agenda[category][new_day] = activities

        return agenda

class Activity(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='activities')
    day = models.ForeignKey(Agenda, related_name='activity',
                            on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.name
