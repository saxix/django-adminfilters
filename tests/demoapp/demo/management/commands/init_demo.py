from urllib.parse import urlencode

from django.core.management import BaseCommand, call_command
from django.db import IntegrityError

from adminfilters.depot.models import StoredFilter


def sample_data():
    from demo.factories import ArtistFactory, BandFactory, CountryFactory, UserFactory
    from demo.models import Artist
    from django.contrib.contenttypes.models import ContentType

    user = UserFactory(username="user")

    uk = CountryFactory(name="United Kingdom")
    australia = CountryFactory(name="Australia")

    acdc = BandFactory(name="AC/DC", active=True)
    geordie = BandFactory(name="Geordie", active=False)

    ArtistFactory(
        name="Angus",
        last_name="Young",
        full_name="Young, Angus",
        active=True,
        year_of_birth=1955,
        bands=[acdc],
        country=uk,
        flags={"v": 1},
    )

    ArtistFactory(
        name="Malcom",
        last_name="Young",
        full_name="Young, Malcom",
        year_of_birth=1953,
        active=True,
        bands=[acdc],
        country=uk,
        flags={"v": 1},
    )

    ArtistFactory(
        name="Phil",
        last_name="Rudd",
        full_name="Rudd, Phil",
        year_of_birth=1954,
        bands=[acdc],
        active=True,
        country=australia,
        flags={"full_name": "Phil Rudd"},
    )

    ArtistFactory(
        name="Brian",
        last_name="Johnson",
        full_name="Johnson, Brian",
        year_of_birth=1947,
        active=True,
        bands=[acdc, geordie],
        country=uk,
        flags={"full_name": "Brian Johnson"},
    )

    ArtistFactory(
        name="Bon",
        last_name="Scott",
        full_name="Scott, Bon",
        year_of_birth=1946,
        active=False,
        bands=[acdc],
        country=uk,
        flags={"full_name": "Bon Scott"},
    )
    ct = ContentType.objects.get_for_model(Artist)
    StoredFilter.objects.update_or_create(
        name="AC/DC",
        owner=user,
        defaults=dict(
            owner=user,
            query_string="?%s" % urlencode({"qs": "bands__name=AC/DC"}),
            content_type=ct,
        ),
    )
    StoredFilter.objects.update_or_create(
        name="QueryString",
        owner=user,
        defaults=dict(
            query_string="?%s"
            % urlencode(
                {
                    "qs": """country__name__istartswith=australia
name=Phil
year_of_birth__gt=1950
Aactive=true""",
                    "qs__negate": "false",
                }
            ),
            content_type=ct,
        ),
    )
    StoredFilter.objects.update_or_create(
        name="Active Artists",
        owner=user,
        defaults=dict(
            query_string="?%s" % urlencode({"qs": "active=true"}), content_type=ct
        ),
    )

    return [acdc, geordie]


class Command(BaseCommand):
    def handle(self, *args, **options):
        from demo.factories import ArtistFactory, DemoModelFieldFactory

        call_command("migrate")
        call_command("collectstatic", interactive=False)
        try:
            ArtistFactory.create_batch(10)
            DemoModelFieldFactory.create_batch(10)
        except IntegrityError:
            pass
        sample_data()
