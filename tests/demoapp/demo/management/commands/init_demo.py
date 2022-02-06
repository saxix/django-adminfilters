from django.core.management import BaseCommand
from django.db import IntegrityError


def sample_data():
    from demo.factories import ArtistFactory, BandFactory, CountryFactory

    uk = CountryFactory(name='United Kingdom')
    australia = CountryFactory(name='Australia')
    acdc = BandFactory(name='AC/DC')
    geordie = BandFactory(name='Geordie')

    ArtistFactory(name='Angus',
                  last_name='Young',
                  full_name='Young, Angus',
                  year_of_birth=1955,
                  bands=[acdc],
                  country=uk, flags={'v': 1})

    ArtistFactory(name='Malcom',
                  last_name='Young',
                  full_name='Young, Malcom',
                  year_of_birth=1953,
                  bands=[acdc],
                  country=uk, flags={'v': 1})

    ArtistFactory(name='Phil',
                  last_name='Rudd',
                  full_name='Rudd, Phil',
                  year_of_birth=1954,
                  bands=[acdc],
                  country=australia, flags={'full_name': 'Phil Rudd'})

    ArtistFactory(name='Brian',
                  last_name='Johnson',
                  full_name='Johnson, Brian',
                  year_of_birth=1947,
                  bands=[acdc, geordie],
                  country=uk, flags={'full_name': 'Brian Johnson'})


class Command(BaseCommand):
    def handle(self, *args, **options):
        from demo.factories import (ArtistFactory, BandFactory,
                                    CountryFactory, DemoModelFieldFactory,)
        try:
            ArtistFactory.create_batch(10)
            DemoModelFieldFactory.create_batch(10)
        except IntegrityError:
            pass

        uk = CountryFactory(name='United Kingdom')
        australia = CountryFactory(name='Australia')
        band = BandFactory(name='AC/DC')
        ArtistFactory(name='Angus',
                      last_name='Young',
                      bands=[band],
                      country=uk, flags={'v': 1})

        ArtistFactory(name='Phil',
                      last_name='Rudd',
                      bands=[band],
                      country=australia, flags={'v': 1})
