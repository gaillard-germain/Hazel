from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.http import Http404
from datetime import date
from registration.models import Family, Child
from .models import Period, Booking, Slot


class SelectChild(View):

    template_name = 'booking/select_child.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            try:
                family = Family.objects.get(user=request.user.id)

            except Family.DoesNotExist:
                return redirect('registration:regfamily')

            children = Child.objects.filter(family=family)

            if not children.count():
                return redirect('registration:regchild_step1')

            context = {'children': children}

            return render(request, self.template_name, context)

        else:
            return redirect('registration:login')


class Modify(View):

    def post(self, request, *args, **kwargs):

        response = {}

        child_id = request.POST.get('child_id')
        command = request.POST.get('command')
        day = request.POST.get('day')

        child = Child.objects.get(id=child_id)

        slot, created = Slot.objects.get_or_create(
            day=date.fromisoformat(day)
        )
        booking, created = Booking.objects.get_or_create(
            child=child,
            slot=slot
        )

        booking.update_booking(command)
        slot.update_slot()

        return JsonResponse(response)


class Calendar(View):

    template_name = 'booking/calendar.html'

    def get(self, request, child_id, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                family = Family.objects.get(user=request.user.id)

            except Family.DoesNotExist:
                return redirect('registration:regfamily')

            try:
                child = Child.objects.get(id=child_id)

            except Child.DoesNotExist:
                raise Http404()

            if child.family != family:
                raise Http404()

            periods = Period.objects.filter(end_date__gte=date.today())

            calendars = {}
            for period in periods:
                calendars[period.name] = period.make_calendar(child)

            context = {
                'child': child,
                'calendars': calendars
            }

            return render(request, self.template_name, context)

        else:
            return redirect('registration:login')
