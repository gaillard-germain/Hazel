from django.db import models
from registration.models import Child


class Date(models.Model):
    day = models.DateField()
    tag = models.CharField(max_length=50)

    def __str__(self):
        return _date(self.day, 'D d F Y')


class Booking(models.Model):
    child = models.ForeignKey(Child, related_name='booking',
                              on_delete=models.CASCADE)
    date = models.ForeignKey(Date, related_name='booking',
                              on_delete=models.CASCADE)
    whole = models.BooleanField(default=True)
    validated = models.BooleanField(default=False)
