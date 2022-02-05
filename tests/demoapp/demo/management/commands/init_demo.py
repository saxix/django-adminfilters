from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("loaddata", "demoproject")
        from demo.factories import (ArtistFactory, BandFactory,
                                    CountryFactory, DemoModelFieldFactory,)
        ArtistFactory.create_batch(10)
        DemoModelFieldFactory.create_batch(10)

        uk = CountryFactory(name='United Kingdom')
        australia = CountryFactory(name='Australia')
        band = BandFactory(name='AC/DC')
        ArtistFactory(name="Angus",
                      last_name="Young",
                      bands=[band],
                      country=uk, flags={"v": 1})

        ArtistFactory(name="Phil",
                      last_name="Rudd",
                      bands=[band],
                      country=australia, flags={"v": 1})
