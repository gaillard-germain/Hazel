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

            try:
                child = Child.objects.get(family=family)

            except Child.DoesNotExist:
                return redirect('registration:regchild_step1')

            children = Child.objects.filter(family=family)

            context = {'children': children}

            return render(request, self.template_name, context)

        else:
            return redirect('registration:login')


class Modify(View):

    def post(self, request, *args, **kwargs):

        response = {}

        child_id = request.POST.get('child_id')
        day_option = request.POST.get('day_option')
        day = request.POST.get('day')

        child = Child.objects.get(id=child_id)

        slot, created = Slot.objects.get_or_create(
            day=date.fromisoformat(day)
        )
        booking, created = Booking.objects.get_or_create(
            child=child,
            slot=slot
        )

        if day_option == 'cancel':
            booking.delete()

        elif day_option == 'full-day' and booking.whole != True:
            booking.whole = True
            booking.save()

        elif day_option == 'half-day' and booking.whole != False:
            booking.whole = False
            booking.save()

        booking_count = Booking.objects.filter(slot=slot).count()

        if booking_count == 0:
            slot.delete()
        elif booking_count >= 60 and not slot.is_full:
            slot.is_full = True
            slot.save()
        elif booking_count < 60 and slot.is_full:
            slot.is_full = False
            slot.save()

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
