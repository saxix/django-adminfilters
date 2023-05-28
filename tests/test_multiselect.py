from functools import partial
from unittest.mock import Mock

import pytest
from demo.models import Artist

from adminfilters.multiselect import IntersectionFieldListFilter, UnionFieldListFilter
from adminfilters.utils import get_query_string


@pytest.fixture
def fixtures(db):
    from demo.factories import ArtistFactory, BandFactory

    band1 = BandFactory(id=1, name="band1")
    band2 = BandFactory(id=2, name="band2")
    band3 = BandFactory(id=3, name="band3")
    ArtistFactory(name="a1", bands=[band1])
    ArtistFactory(name="a2", bands=[band2])
    ArtistFactory(name="a3", bands=[band3])
    ArtistFactory(name="a12", bands=[band1, band2])
    ArtistFactory(name="a23", bands=[band2, band3])


@pytest.mark.parametrize(
    "value,expected",
    [
        ("1", ["a1", "a12"]),
        ("2", ["a12", "a2", "a23"]),
        ("1,2", ["a1", "a12", "a2", "a23"]),
        ("2,3", ["a12", "a2", "a23", "a3"]),
        ("", ["a1", "a12", "a2", "a23", "a3"]),
    ],
)
def test_union(fixtures, value, expected):
    f = UnionFieldListFilter(
        Artist._meta.get_field("bands"),
        None,
        {"bands_filter": value},
        None,
        None,
        "bands",
    )
    result = f.queryset(None, Artist.objects.order_by("name"))
    value = list(result.order_by("name").values_list("name", flat=True))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("1", ["a1", "a12"]),
        ("2", ["a12", "a2", "a23"]),
        ("1,2", ["a12"]),
        ("2,3", ["a23"]),
        ("", ["a1", "a12", "a2", "a23", "a3"]),
    ],
)
def test_intersection(fixtures, value, expected):
    f = IntersectionFieldListFilter(
        Artist._meta.get_field("bands"),
        None,
        {"bands_filter": value},
        None,
        None,
        "bands",
    )
    result = f.queryset(None, Artist.objects.order_by("name"))
    value = list(result.order_by("name").values_list("name", flat=True))
    assert value == expected


def test_choices(fixtures):
    params = {"bands_filter": "1,2"}
    f = IntersectionFieldListFilter(
        Artist._meta.get_field("bands"), None, params, None, None, "bands"
    )
    # result = f.queryset(None, Artist.objects.order_by('name'))
    cl = Mock(
        get_query_string=partial(get_query_string, Mock(GET=params)), params=params
    )
    choices = list(f.choices(cl))
    assert len(choices) == 4
    assert choices[0] == {"display": "All", "query_string": "?", "selected": False}
    assert choices[1] == {
        "display": "band1",
        "query_string": "?bands_filter=2",
        "selected": True,
    }
    assert choices[2] == {
        "display": "band2",
        "query_string": "?bands_filter=1",
        "selected": True,
    }
