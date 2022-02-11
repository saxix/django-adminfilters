import pytest
from demo.models import Artist, Country
from demo.urls import public_site

from adminfilters.autocomplete import AutoCompleteFilter


@pytest.fixture
def fixtures(db):
    from demo.factories import ArtistFactory
    ArtistFactory(name='a1', country__name='c1')
    ArtistFactory(name='a2', country__name='c1')
    ArtistFactory(name='b1', country__name='c2')
    ArtistFactory(name='c1', country__name='c2')


@pytest.mark.parametrize('value', ['c1', 'c2'])
def test_filter(fixtures, value):
    country = Country.objects.get(name=value)
    f = AutoCompleteFilter(Artist._meta.get_field('country'), None,
                           {'country__exact': country, 'name__isnull': ''},
                           Artist, public_site._registry[Artist], 'country')
    qs = f.queryset(None, Artist.objects.all())
    result = set(qs.values_list('country__name', flat=True))
    assert result == {value}
