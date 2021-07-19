from django.db import models
from django.template.defaultfilters import date as _date
from datetime import date, timedelta
from registration.models import Child


class Period(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'Période'

    def __str__(self):
        return self.name

    def make_calendar(self, child):
        """ Returns a dict {month: {weekday: [date]}} of the period"""

        calendar = {}
        current = self.start_date + timedelta(days=1)

        if self.name == 'Périscolaire':
            excluded = [0, 1, 3, 4, 5, 6]
        else:
            excluded = [5, 6]

        while self.end_date != current:

            month = _date(current, 'F Y')
            weekday = _date(current, 'D')

            if current.weekday() not in excluded and current > date.today():
                if month not in calendar:
                    calendar[month] = {}

                if weekday not in calendar[month]:
                    calendar[month][weekday] = {}

                try:
                    slot = Slot.objects.get(day=current)

                    try:
                        booking = Booking.objects.get(slot=slot, child=child)
                        calendar[month][weekday][current] = booking

                    except Booking.DoesNotExist:
                        if slot.is_full:
                            calendar[month][weekday][current] = 'full'
                        else:
                            calendar[month][weekday][current] = None

                except Slot.DoesNotExist:
                    calendar[month][weekday][current] = None

            current += timedelta(days=1)

        return calendar


class Slot(models.Model):
    day = models.DateField(verbose_name='Date')
    is_full = models.BooleanField(default=False, verbose_name='Complet')

    class Meta:
        ordering = ['day']
        verbose_name = 'Créneau'
        verbose_name_plural = 'Créneaux'

    def __str__(self):
        return _date(self.day, 'd F Y')

    def update_slot(self):
        booking_count = Booking.objects.filter(slot=self).count()

        if booking_count == 0:
            self.delete()
        elif booking_count >= 60 and not self.is_full:
            self.is_full = True
            self.save()
        elif booking_count < 60 and self.is_full:
            self.is_full = False
            self.save()


class Booking(models.Model):
    child = models.ForeignKey(Child, related_name='booking',
                              on_delete=models.CASCADE, verbose_name='Enfant')
    slot = models.ForeignKey(Slot, related_name='booking',
                             on_delete=models.CASCADE)
    whole = models.BooleanField(default=True, verbose_name='Journée complète')
    validated = models.BooleanField(default=False, verbose_name='Validé')

    class Meta:
        verbose_name = 'Réservation'

    def __str__(self):
        return '{} {}'.format(self.child, self.slot)

    def update_booking(self, command):
        if command == 'cancel':
            self.delete()

        elif command == 'full-day' and not self.whole:
            self.whole = True
            self.save()

        elif command == 'half-day' and self.whole:
            self.whole = False
            self.save()
