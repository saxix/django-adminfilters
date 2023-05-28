import pytest
from demo.factories import ArtistFactory
from demo.models import Artist

from adminfilters.json import JsonFieldFilter


@pytest.fixture
def fixtures(db):
    ArtistFactory(flags={"v": 1})
    ArtistFactory(flags={"v": 1})
    ArtistFactory(flags={"v": 2})
    ArtistFactory(flags={"v": "2"})
    ArtistFactory(flags={})


def test_JsonFieldFilter(fixtures):
    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "1",
            "flags__negate": "false",
            "flags__options": "e",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == [
        1,
        1,
    ]

    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "1",
            "flags__negate": "false",
            "flags__options": "i",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == [
        1,
        1,
        None,
    ]
    # negate
    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "1",
            "flags__negate": "true",
            "flags__options": "e",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    # this is a Django bug. It should returns [2, "2"]
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == [
        "2",
        2,
    ]

    # negate / include
    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "1",
            "flags__negate": "true",
            "flags__options": "i",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    # this is a Django bug. It should returns [2, "2"]
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == [
        "2",
        2,
        None,
    ]

    # cast to int
    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "2",
            "flags__negate": "false",
            "flags__type": "num",
            "flags__options": "e",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == [2]

    # cast to char
    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "2",
            "flags__negate": "false",
            "flags__type": "str",
            "flags__options": "e",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == ["2"]

    # cast to char/include
    f = JsonFieldFilter(
        "json",
        None,
        {
            "flags__key": "v",
            "flags__value": "2",
            "flags__negate": "false",
            "flags__type": "str",
            "flags__options": "i",
        },
        None,
        None,
        "flags",
    )
    result = f.queryset(None, Artist.objects.all())
    assert list(result.order_by("flags__v").values_list("flags__v", flat=True)) == [
        "2",
        None,
    ]
