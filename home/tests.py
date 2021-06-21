from django.test import TestCase
from django.urls import reverse
from django.template.defaultfilters import date as _date
from datetime import date, datetime
from .models import Agenda, Category, Activity


class IndexPageTestCase(TestCase):

    def setUp(self):
        self.agenda = Agenda.objects.create(entry=date.today())
        self.category = Category.objects.create(name='FAKE')
        self.activity = Activity.objects.create(
            name='Fake activity',
            day=self.agenda,
            start_time=datetime.now().time(),
            end_time=datetime.now().time()
        )
        self.activity.categories.add(self.category)

    def test_index_page_returns_200(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_agenda_conform_to_expected(self):
        response = self.client.get(reverse('home:index'))
        day = _date(self.agenda.entry, 'D d F')
        result = self.activity.name
        self.assertEqual(
            response.context['agenda'][self.category][day][0].name, result
        )
