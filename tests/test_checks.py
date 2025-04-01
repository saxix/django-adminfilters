from unittest.mock import MagicMock, Mock

from demo.admin import ArtistModelAdmin
from demo.models import Artist
from demo.urls import public_site

from adminfilters.autocomplete import LinkedAutoCompleteFilter


class Test1(ArtistModelAdmin):
    pass


class Test2(ArtistModelAdmin):
    list_filter = (
        ("favourite_city__region__country", LinkedAutoCompleteFilter.factory(title="Favourite Country")),
        ("favourite_city__region", LinkedAutoCompleteFilter.factory(title="Favourite Region", parent="missing")),
    )


def test_check_in():
    from demo.urls import public_site

    ma = public_site._registry[Artist]
    ma.check()


def test_check1():
    assert not Test1(Artist, public_site).check()


def test_check2():
    assert Test2(Artist, public_site).check()
