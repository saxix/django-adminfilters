import pytest
from demo.models import Artist

from adminfilters.multiselect import (IntersectionFieldListFilter,
                                      UnionFieldListFilter,)


@pytest.fixture
def fixtures(db):
    from demo.factories import ArtistFactory, BandFactory
    band1 = BandFactory(id=1, name='band1')
    band2 = BandFactory(id=2, name='band2')
    band3 = BandFactory(id=3, name='band3')
    ArtistFactory(name='a1', bands=[band1])
    ArtistFactory(name='a2', bands=[band2])
    ArtistFactory(name='a3', bands=[band3])
    ArtistFactory(name='a12', bands=[band1, band2])
    ArtistFactory(name='a23', bands=[band2, band3])


@pytest.mark.parametrize('value,expected', [('1', ['a1', 'a12']),
                                            ('2', ['a12', 'a2', 'a23']),
                                            ('1,2', ['a1', 'a12', 'a2', 'a23']),
                                            ('2,3', ['a12', 'a2', 'a23', 'a3']),
                                            ])
def test_union(fixtures, value, expected):
    f = UnionFieldListFilter(Artist._meta.get_field('bands'), None,
                             {'bands_filter': value}, None, None, 'bands')
    result = f.queryset(None, Artist.objects.order_by('name'))
    value = list(result.order_by('name').values_list('name', flat=True))
    assert value == expected


@pytest.mark.parametrize('value,expected', [('1', ['a1', 'a12']),
                                            ('2', ['a12', 'a2', 'a23']),
                                            ('1,2', ['a12']),
                                            ('2,3', ['a23']),
                                            ])
def test_intersection(fixtures, value, expected):
    f = IntersectionFieldListFilter(Artist._meta.get_field('bands'), None,
                                    {'bands_filter': value}, None, None, 'bands')
    result = f.queryset(None, Artist.objects.order_by('name'))
    value = list(result.order_by('name').values_list('name', flat=True))
    assert value == expected
#
