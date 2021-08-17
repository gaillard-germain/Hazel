from django.db import models
from django.template.defaultfilters import date as _date
from datetime import date, timedelta

from registration.models import Child, Category


class Period(models.Model):
    """ Holidays periods """

    name = models.CharField(max_length=50, verbose_name='Nom')
    start_date = models.DateField(verbose_name='Date début')
    end_date = models.DateField(verbose_name='Date fin')

    class Meta:
        verbose_name = "Période d'ouverture"
        verbose_name_plural = "Périodes d'ouverture"
        constraints = [
            models.UniqueConstraint(fields=['name'],
                                    name='unique_period'),
        ]

    def __str__(self):
        return self.name

    def get_days(self, weekday):
        """ return a list of all given weekday in the period
            (0=monday...6=sunday)"""
        all_days = []
        current = self.start_date + timedelta(days=1)
        while current != self.end_date:
            if current.weekday() == weekday:
                all_days.append(current)
            current += timedelta(days=1)
        return all_days

    def make_calendar(self, child, wednesday=[]):
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

            if (current.weekday() not in excluded and
                    current > date.today() and current not in wednesday):
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
    """ Slot for booking (the only interest is to store is_full field)"""

    day = models.DateField(verbose_name='Date')
    is_full = models.BooleanField(default=False, verbose_name='Complet')

    class Meta:
        ordering = ['day']
        verbose_name = 'Jour'
        constraints = [
            models.UniqueConstraint(fields=['day'],
                                    name='unique_slot'),
        ]

    def __str__(self):
        return _date(self.day, 'd F Y')

    def update_slot(self):
        """ Updates slot state when user booked a day """
        booking_count = Booking.objects.filter(slot=self).count()
        activity_count = Activity.objects.filter(slot=self).count()

        if booking_count == 0 and activity_count == 0:
            self.delete()
        elif booking_count >= 60 and not self.is_full:
            self.is_full = True
            self.save()
        elif booking_count < 60 and self.is_full:
            self.is_full = False
            self.save()


class Booking(models.Model):
    """ Booking book """

    child = models.ForeignKey(Child, related_name='booking',
                              on_delete=models.CASCADE, verbose_name='Enfant')
    slot = models.ForeignKey(Slot, related_name='booking',
                             on_delete=models.CASCADE, verbose_name='Créneau')
    whole = models.BooleanField(default=True, verbose_name='Journée complète')
    validated = models.BooleanField(default=False, verbose_name='Validé')

    class Meta:
        verbose_name = 'Réservation'
        constraints = [
            models.UniqueConstraint(fields=['child', 'slot'],
                                    name='unique_booking'),
        ]

    def __str__(self):
        return '{} {}'.format(self.child, self.slot)

    def update_booking(self, command):
        """ updates booking when user cancelled or booked a day """

        if command == 'cancel':
            self.delete()

        elif command == 'full-day' and not self.whole:
            self.whole = True
            self.save()

        elif command == 'half-day' and self.whole:
            self.whole = False
            self.save()


class Activity(models.Model):
    """ Planned activities to entertain children """

    name = models.CharField(max_length=100, verbose_name='Nom')
    categories = models.ManyToManyField(Category, related_name='activities',
                                        verbose_name='Catégorie')
    slot = models.ForeignKey(Slot, related_name='activities',
                             on_delete=models.CASCADE, verbose_name='Date',
                             null=True)
    start_time = models.TimeField(verbose_name='Heure début')
    end_time = models.TimeField(verbose_name='Heure fin')
    extra_charge = models.DecimalField(max_digits=4, decimal_places=2,
                                       verbose_name='Supplément tarif',
                                       blank=True, null=True)

    class Meta:
        ordering = ['start_time']
        verbose_name = 'Activité'

    def __str__(self):
        return self.name

    @classmethod
    def make_agenda(cls):
        all_categories = Category.objects.all()
        slots = Slot.objects.filter(day__gte=date.today())
        agenda = {}

        for category in all_categories:
            agenda[category] = {}
            for slot in slots:
                new_day = _date(slot.day, 'D d F')
                activities = cls.objects.filter(slot=slot.id)
                activities = activities.filter(categories=category)
                if activities:
                    agenda[category][new_day] = activities

        return agenda
