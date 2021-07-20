from django.db import models
from django.template.defaultfilters import date as _date
from datetime import date


class Price(models.Model):
    family_quotient = models.CharField(max_length=15,
                                       verbose_name='Quotient familial')
    day = models.DecimalField(max_digits=4, decimal_places=2,
                              verbose_name='Prix journée')
    half_day = models.DecimalField(max_digits=4, decimal_places=2,
                                   verbose_name='Prix demi-journée')

    class Meta:
        ordering = ['day']
        verbose_name = 'Tarif'

    def __str__(self):
        return 'Quotient familial {}'.format(self.family_quotient)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nom')
    age_min = models.IntegerField()
    age_max = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Catégorie'

    def __str__(self):
        return self.name


class Agenda(models.Model):
    entry = models.DateField(verbose_name='Date')

    class Meta:
        ordering = ['entry']
        verbose_name = "Page de l'agenda"
        verbose_name_plural = "Pages de l'agenda"

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
    name = models.CharField(max_length=100, verbose_name='Nom')
    categories = models.ManyToManyField(Category, related_name='activities',
                                        verbose_name='Catégorie')
    day = models.ForeignKey(Agenda, related_name='activity',
                            on_delete=models.CASCADE, verbose_name='Date')
    start_time = models.TimeField(verbose_name='Heure début')
    end_time = models.TimeField(verbose_name='Heure fin')

    class Meta:
        ordering = ['start_time']
        verbose_name = 'Activité'

    def __str__(self):
        return self.name
