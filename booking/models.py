from django.db import models
from django.template.defaultfilters import date as _date
from datetime import date, timedelta
from registration.models import Child


class Period(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def make_calendar(self):
        """ Returns a dict {month: {weekday: [date]}} of the period"""

        calendar = {}
        current = self.start_date + timedelta(days=1)

        if self.name == 'periscolaire':
            excluded = [0, 1, 3, 4, 5, 6]
        else:
            excluded = [5, 6]

        while self.end_date != current:

            month = _date(current, 'F Y')
            weekday = _date(current, 'D')

            if current.weekday() not in excluded:
                if month not in calendar:
                    calendar[month] = {}

                if weekday not in calendar[month]:
                    calendar[month][weekday] = []

                calendar[month][weekday].append(current)

            current += timedelta(days=1)

        return calendar


class Booking(models.Model):
    child = models.ForeignKey(Child, related_name='booking',
                              on_delete=models.CASCADE)
    day = models.DateField()
    whole = models.BooleanField(default=True)
    validated = models.BooleanField(default=False)
