import pytest
from demo.models import DemoModelField

from adminfilters.querystring import QueryStringFilter


@pytest.fixture
def fixtures(db):
    from demo.utils import DATA

    for i in range(1, 5):
        values = DATA.copy()
        values["unique"] = i
        values["logic"] = bool(i % 2)
        values["json"] = {
            "char": chr(ord("a") + i),
            "integer": i * 100,
            "float": i * 1.0,
        }

        DemoModelField.objects.create(**values)


@pytest.mark.parametrize(
    "op,expected,error",
    [
        ("unique=1", "1", None),
        ("unique__in=1,2,3", "1,2,3", None),
        ("!unique=2", "1,3,4", None),
        ("logic=true", "1,3", None),
        ("logic=false", "2,4", None),
        ("!logic=false", "1,3", None),
        ("json__char=b", "1", None),
        ("#json__integer=100", "1", None),
        ("!#json__integer=100", "2,3,4", None),
        (".json__float=1.0", "1", None),
        ("logic__in=true,false", "1,2,3,4", None),
        ("wrong=1", "1,2,3,4", "Unknown field 'wrong'"),
        ("logic__x=1", "1,2,3,4", "Unsupported lookup: 'x'"),
    ],
)
def test_QueryStringFilter(fixtures, op, expected, error, caplog):
    f = QueryStringFilter(None, {"qs": op}, DemoModelField, None)
    result = f.queryset(None, DemoModelField.objects.all())
    value = list(result.values_list("unique", flat=True))
    assert value == expected.split(","), value
    assert f.error_message == error


def test_media():
    assert QueryStringFilter.factory(title="Title")(
        None, {}, DemoModelField, None
    ).media
