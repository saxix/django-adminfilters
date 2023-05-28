import pytest

from adminfilters.utils import get_query_string


@pytest.mark.parametrize(
    "qs,new_params,remove,result",
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
