from django.shortcuts import render
from django.views import View
from .models import Price, Agenda


class Index(View):

    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        prices = Price.objects.all()
        agenda = Agenda.make_agenda()

        context = {
            'prices': prices,
            'agenda': agenda
        }
        return render(request, self.template_name, context)
