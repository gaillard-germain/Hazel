from django.test import TestCase
from django.urls import reverse
from django.template.defaultfilters import date as _date
from datetime import date, datetime
from registration.models import Category
from booking.models import Slot, Activity
from .models import Price
import decimal


class IndexPageTestCase(TestCase):

    def setUp(self):
        self.price = Price.objects.create(family_quotient='fake',
                                          day=2.55, half_day=1.65)
        self.slot = Slot.objects.create(day=date.today())
        self.category = Category.objects.create(name='FAKE', age_min=5,
                                                age_max=8)
        self.activity = Activity.objects.create(
            name='Fake activity',
            slot=self.slot,
            start_time=datetime.now().time(),
            end_time=datetime.now().time()
        )
        self.activity.categories.add(self.category)

    def test_index_page_returns_200(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_agenda_conform_to_expected(self):
        response = self.client.get(reverse('home:index'))
        day = _date(self.slot.day, 'D d F')
        result = self.activity.name
        self.assertEqual(
            response.context['agenda'][self.category][day][0].name, result
        )

    def test_index_page_prices_conform_to_expected(self):
        response = self.client.get(reverse('home:index'))
        print('AAAh')
        print(type(response.context['prices'][0].day))
        self.assertEqual(
            response.context['prices'][0].family_quotient,
            self.price.family_quotient
        )
        self.assertIsInstance(
            response.context['prices'][0].day, decimal.Decimal
        )


class LegalNoticePageTestCase(TestCase):

    def test_legal_notice_page_return_200(self):
        response = self.client.get(reverse('home:legal_notice'))
        self.assertEqual(response.status_code, 200)
