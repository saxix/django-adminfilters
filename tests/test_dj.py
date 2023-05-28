import pytest
from demo.models import Artist

from adminfilters.dj import DjangoLookupFilter


@pytest.fixture
def fixtures(db):
    from demo.factories import ArtistFactory

    ArtistFactory(name="a1", active=True)
    ArtistFactory(name="a2", active=True)
    ArtistFactory(name="b1", active=True)
    ArtistFactory(name="c1", active=False)


def test_media():
    assert DjangoLookupFilter.factory(title="Title")(None, {}, Artist, None).media


@pytest.mark.parametrize(
    "key,value,negate,expected",
    [
        ("name", "a1", False, ["a1"]),
        ("name__endswith", "2", False, ["a2"]),
        ("name__in", "a1,a2", False, ["a1", "a2"]),
        ("active", "true", False, ["a1", "a2", "b1"]),
        ("active", "false", False, ["c1"]),
        ("active", "false", True, ["a1", "a2", "b1"]),
        ("xx", "zz", True, ["a1", "a2", "b1", "c1"]),
    ],
)
def test_value_filter(fixtures, key, value, negate, expected):
    f = DjangoLookupFilter(
        None,
        {"dj__key": key, "dj__value": value, "dj__negate": str(negate).lower()},
        Artist,
        None,
    )

    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected
