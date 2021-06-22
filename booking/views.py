from django.shortcuts import render, redirect
from django.views import View
from registration.models import Family, Child


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
                child = Child.objects.get(family=family)

            except Child.DoesNotExist:
                return redirect('registration:regchild_step1')

        else:
            return redirect('registration:login')


        return self.post(request, *args, **kwargs)
