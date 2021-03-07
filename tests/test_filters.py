import pytest

from adminfilters.filters import TextFieldFilter, ForeignKeyFieldFilter
from demoproject.demoapp.models import DemoModelField, DemoRelated, DemoModel

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
    "null_logic": True,
    "logic": False,
    "date": "2013-01-29",
    "integer": 888888,
    "email": "s.apostolico@gmail.com",
    "choices": 2
}


@pytest.fixture
def fixtures(db):
    DemoModelField.objects.create(char="a1", unique=1, **DATA)
    related = DemoRelated.objects.create(name='related1')
    DemoModel.objects.create(demo_related=related, name='name1')
    return DemoModelField.objects.create(char="a2", unique=2, **DATA)


def test_TextFieldFilter(fixtures, rf):
    f = TextFieldFilter.factory('char')

    qs = f(None, {'char|iexact': 'www'}, None, None).queryset(None, DemoModelField.objects.all())
    assert not qs.exists()

    qs = f(None, {'char|iexact': 'a1'}, None, None).queryset(None, DemoModelField.objects.all())
    assert qs.exists()


def test_ForeignKeyFieldFilter(fixtures, rf):
    f = ForeignKeyFieldFilter.factory('demo_related__name__istartswith')

    qs = f(None, {'demo_related|name|istartswith': 'www'}, None, None).queryset(None, DemoModel.objects.all())
    assert not qs.exists()

    qs = f(None, {'demo_related|name|istartswith': 'related1'}, None, None).queryset(None, DemoModel.objects.all())
    assert qs.exists()
