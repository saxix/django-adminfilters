import pytest
from demo.models import DemoModelField

from adminfilters.querystring import QueryStringFilter

DATA = {
    "nullable": "bbbb",
    "float": 10.1,
    "generic_ip": "192.168.10.2",
    "url": "https://github.com/saxix/django-adminfilters",
    "decimal": "22.2",
    "time": "19:00:35",
    "blank": "",
    "datetime": "2013-01-01T02:18:33Z",
    "not_editable": None,
    "bigint": 333333333,
    "text": "lorem ipsum",
    "logic": False,
    "date": "2013-01-29",
    "integer": 888888,
    "email": "s.apostolico@gmail.com",
    "choices": 2,
    "flags": {},
}


@pytest.fixture
def fixtures(db):
    for i in range(1, 5):
        values = DATA.copy()
        values['unique'] = i
        DemoModelField.objects.create(**values)


@pytest.mark.parametrize("op,expected", [("unique=1", "1"),
                                         ("unique__in=1,2,3", "1,2,3"),
                                         ("!unique=2", "1,3,4"),
                                         ])
def test_QueryStringFilter(fixtures, op, expected):
    f = QueryStringFilter(None, {"qs": op}, None, None)
    result = f.queryset(None, DemoModelField.objects.all())
    value = list(result.values_list("unique", flat=True))
    assert value == expected.split(","), value
