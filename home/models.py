from django.db import models

class Price(models.Model):
    family_quotient = models.CharField(max_length=15)
    day = models.DecimalField(max_digits=4, decimal_places=2)
    half_day = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return 'Quotient familial {}'.format(self.family_quotient)
