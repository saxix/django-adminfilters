import pytest
from demo.models import Artist

from adminfilters.compat import DJANGO_MAJOR
from adminfilters.filters import MultiValueFilter, ValueFilter


@pytest.fixture
def fixtures(db):
    from demo.factories import ArtistFactory

    ArtistFactory(name="a1")
    ArtistFactory(name="a2")
    ArtistFactory(name="b1")
    ArtistFactory(name="c1")


def test_media():
    assert ValueFilter.factory(title="Title")(
        None, None, {}, None, None, "unique"
    ).media


@pytest.mark.parametrize(
    "value,negate,expected",
    [
        ("n", False, []),
        ("a1", False, ["a1"]),
        ("a1", True, ["a2", "b1", "c1"]),
    ],
)
def test_value_filter(fixtures, value, negate, expected):
    f = ValueFilter(
        Artist._meta.get_field("name"),
        None,
        {"name__exact": value, "name__exact__negate": str(negate).lower()},
        None,
        None,
        "name",
    )

    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected


def test_factory(fixtures):
    F = ValueFilter.factory(title="CustomTitle")
    f = F(
        Artist._meta.get_field("name"),
        None,
        {"name__exact": "a1", "name__exact__negate": "false"},
        None,
        None,
        "name",
    )

    assert f.value() == ["a1", False]
    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == ["a1"]


@pytest.mark.parametrize(
    "value,negate,expected",
    [
        ("n", False, []),
        ("a1", False, ["a1"]),
        ("a1", True, ["a2", "b1", "c1"]),
    ],
)
def test_MultiValueTextFieldFilter(fixtures, value, negate, expected):
    if DJANGO_MAJOR < 5:
        val = value
    else:
        val = [value]
    f = MultiValueFilter(
        Artist._meta.get_field("name"),
        None,
        {"name__in": val, "name__in__negate": str(negate).lower()},
        None,
        None,
        "name",
    )
    assert f.value() == [[value], negate]
    result = f.queryset(None, Artist.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected
