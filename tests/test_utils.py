import pytest

from adminfilters.utils import get_query_string, parse_bool, get_field_by_path
from demo.factories import DemoModelFieldFactory
from demo.models import DemoModelField, Region


@pytest.mark.parametrize(
    ("value", "result"),
    (
           ( "t", True),
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            (True, True),
            (0, False),
            (11, 11),
    ),
)
def test_parse_bool(value, result):
    assert parse_bool(value) == result


@pytest.mark.parametrize(
    ("qs", "new_params", "remove", "result"),
    (
            ("", {}, [], "?"),
            ("?a=1&b=2&c=3", {}, [], "?a=1&b=2&c=3"),
            ("?a=1&b=2&c=3", {}, ["b"], "?a=1&c=3"),
            ("?a=1&b=2&c=3", {"c": 44}, [], "?a=1&b=2&c=44"),
            ("?a=1&b=2&c=3", {"c": None}, [], "?a=1&b=2"),
            ("?a=1&b=2&c=3", {"x": None}, [], "?a=1&b=2&c=3"),
            ("?a=1&b=2&c=3", None, None, "?a=1&b=2&c=3"),
    ),
)
def test_get_query_string(rf, qs, new_params, remove, result):
    request = rf.get(qs)
    ret = get_query_string(request, new_params, remove)
    assert ret == result


def test_get_field_by_path():
    # record = DemoModelFieldFactory()
    assert get_field_by_path(DemoModelField, "char")
    assert get_field_by_path(Region, "country.name")
    assert get_field_by_path(Region, "country.wrong")
    with pytest.raises(ValueError):
        assert get_field_by_path(None, "country.wrong")
