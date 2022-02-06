import pytest
from demo.models import Artist, DemoModelField

from adminfilters.lookup import GenericLookupFieldFilter


@pytest.fixture
def fixtures(db):
    from demo.utils import DATA
    DemoModelField.objects.create(char='a1', unique=1, **DATA)
    DemoModelField.objects.create(char='a2', unique=2, **DATA)
    DemoModelField.objects.create(char='b1', unique=3, **DATA)


@pytest.fixture
def artist(db):
    from demo.factories import ArtistFactory
    a = ArtistFactory(name='name1')
    ArtistFactory(name='name2')
    ArtistFactory(name='name3')
    return a


def test_media():
    assert GenericLookupFieldFilter.factory('char')(None, {}, None, None).media


def test_GenericLookupFieldFilter(fixtures, rf):
    f = GenericLookupFieldFilter.factory('char')

    qs = f(None, {'char>exact': 'www|false'}, None, None).queryset(None, DemoModelField.objects.all())
    assert not qs.exists()

    qs = f(None, {'char>exact': 'a1|false'}, None, None).queryset(None, DemoModelField.objects.all())
    assert qs.first().char == 'a1'

    qs = f(None, {'char>exact': 'a1|true'}, None, None).queryset(None, DemoModelField.objects.all())
    assert qs.first().char == 'a2'


def test_GenericLookupFieldFilterNegate(artist, rf):
    f = GenericLookupFieldFilter.factory('country__name__istartswith')

    qs = f(None, {'country>name>istartswith': 'www|false'}, None, None).queryset(None, Artist.objects.all())
    assert not qs.exists()

    qs = f(None,
           {'country>name>istartswith': f'{artist.country.name}|false'},
           None, None).queryset(None, Artist.objects.all())
    assert qs.first().country == artist.country
