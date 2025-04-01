from unittest.mock import Mock

import pytest
from demo.factories import ArtistFactory
from demo.models import Artist
from pyquery import PyQuery

from adminfilters.filters import JsonFieldFilter


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
    result = f.queryset(Mock(), Artist.objects.all())
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


def test_querystring(fixtures, django_app):
    res = django_app.get(
        "/demo/artist/?&flags__key=v&flags__value=1&flags__type=any&flags__options=e&flags__negate=false"
    )
    pq = PyQuery(res.content)
    jt1 = pq("input[type=text][name=key][data-group=flags]")
    assert jt1.val() == "v"
    jt2 = pq("input[type=text][name=value][data-group=flags]")
    assert jt2.val() == "1"


#     http://127.0.0.1:8000/demo/artist/?&flags__key=v&flags__value=1&flags__type=any&flags__options=e&flags__negate=false
