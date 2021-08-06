from django.shortcuts import render
from django.views import View
from .models import Price

from booking.models import Activity


class Index(View):
    """ A view to display general information """

    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        prices = Price.objects.all()
        agenda = Activity.make_agenda()

        context = {
            'prices': prices,
            'agenda': agenda
        }
        return render(request, self.template_name, context)


class LegalNotice(View):
    """ A view to display legal notice """

    template_name = 'home/legalnotice.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
