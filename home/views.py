from django.shortcuts import render
from django.views import View
from .models import Price


class Index(View):

    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        prices = Price.objects.all()
        return render(request, self.template_name, {'prices': prices})
