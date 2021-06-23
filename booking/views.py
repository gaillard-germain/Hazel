from django.shortcuts import render, redirect
from django.views import View
from datetime import date
from registration.models import Family, Child
from .models import Period


class Calendar(View):

    template_name = 'booking/calendar.html'

    def post(self, request, *args, **kwargs):

        context = {}

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                family = Family.objects.get(user=request.user.id)

            except Family.DoesNotExist:
                return redirect('registration:regfamily')

            try:
                children = Child.objects.filter(family=family)

            except Child.DoesNotExist:
                return redirect('registration:regchild_step1')

            periods = Period.objects.filter(end_date__gte=date.today())

            calendars = {}
            for period in periods:
                calendars[period.name] = period.make_calendar()

            context = {'calendars': calendars}

            return render(request, self.template_name, context)

        else:
            return redirect('registration:login')
