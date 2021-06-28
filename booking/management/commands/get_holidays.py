from django.core.management.base import BaseCommand
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from booking.models import Period


class Command(BaseCommand):
    """ Custom command to get the holidays of the current school year from
        https://data.education.gouv.fr/api and save it to the database.
        ./manage.py get_holidays to run (! it will delete former periods!) """

    def get_school_year(self):
        if date.today().month < 9:
            year1 = (date.today() - relativedelta(years=1)).year
            year2 = date.today().year
        else:
            year1 = date.today().year
            year2 = (date.today() + relativedelta(years=1)).year

        return year1, year2

    def handle(self, *args, **options):
        year1, year2 = self.get_school_year()

        query = 'https://data.education.gouv.fr/api/records/1.0/search/?\
dataset=fr-en-calendrier-scolaire&q=&facet=description&\
facet=population&facet=start_date&facet=end_date&\
facet=location&facet=zones&\
facet=annee_scolaire&refine.population=%C3%89l%C3%A8ves&\
refine.location=Bordeaux&refine.zones=Zone+A&\
refine.annee_scolaire={}-{}&\
timezone=Europe%2FParis'.format(year1, year2)

        response = requests.get(query)
        response = response.json()

        Period.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted former periods'))

        for record in response['records']:
            fields = record['fields']
            name = fields['description']
            start_date = date.fromisoformat(fields['start_date'].split('T')[0])
            end_date = date.fromisoformat(fields['end_date'].split('T')[0])

            period = Period.objects.create(name=name, start_date=start_date,
                                           end_date=end_date)

            self.stdout.write(self.style.SUCCESS(
                'Successfully create {} period'.format(period.name))
            )

        start_date = date.fromisoformat('{}-09-01'.format(year1))
        end_date = date.fromisoformat('{}-07-01'.format(year2))

        period = Period.objects.create(name='Périscolaire',
                                       start_date=start_date,
                                       end_date=end_date)

        self.stdout.write(self.style.SUCCESS(
                'Successfully create {} period'.format(period.name))
            )
