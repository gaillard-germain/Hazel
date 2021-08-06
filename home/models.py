from django.db import models
from django.template.defaultfilters import date as _date
from datetime import date


class Price(models.Model):
    """ Prices for day or half-day in terms of family quotient """

    family_quotient = models.CharField(max_length=15,
                                       verbose_name='Quotient familial')
    day = models.DecimalField(max_digits=4, decimal_places=2,
                              verbose_name='Prix journée')
    half_day = models.DecimalField(max_digits=4, decimal_places=2,
                                   verbose_name='Prix demi-journée')

    class Meta:
        ordering = ['day']
        verbose_name = 'Tarif'
        constraints = [
            models.UniqueConstraint(fields=['family_quotient'],
                                    name='unique_quotient'),
        ]

    def __str__(self):
        return 'Quotient familial {}'.format(self.family_quotient)
