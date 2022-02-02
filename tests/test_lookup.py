import pytest
from demoproject.demoapp.models import DemoModel, DemoModelField, DemoRelated

from adminfilters.lookup import GenericLookupFieldFilter

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
    related1 = DemoRelated.objects.create(name='related1')
    related2 = DemoRelated.objects.create(name='related2')
    DemoModel.objects.create(demo_related=related1, name='name1')
    DemoModel.objects.create(demo_related=related2, name='name2')
    DemoModelField.objects.create(char="a2", unique=2, **DATA)
    DemoModelField.objects.create(char="b1", unique=3, **DATA)


def test_media(fixtures, rf):
    assert GenericLookupFieldFilter.factory('char')(None, {}, None, None).media


def test_GenericLookupFieldFilter(fixtures, rf):
    f = GenericLookupFieldFilter.factory('char')

    qs = f(None, {'char>exact': 'www|false'}, None, None).queryset(None, DemoModelField.objects.all())
    assert not qs.exists()

    qs = f(None, {'char>exact': 'a1|false'}, None, None).queryset(None, DemoModelField.objects.all())
    assert qs.first().char == 'a1'

    qs = f(None, {'char>exact': 'a1|true'}, None, None).queryset(None, DemoModelField.objects.all())
    assert qs.first().char == 'a2'


def test_GenericLookupFieldFilterNegate(fixtures, rf):
    f = GenericLookupFieldFilter.factory('demo_related__name__istartswith')

    qs = f(None, {'demo_related>name>istartswith': 'www|false'}, None, None).queryset(None, DemoModel.objects.all())
    assert not qs.exists()

    qs = f(None, {'demo_related>name>istartswith': 'related1|false'}, None, None).queryset(None,
                                                                                           DemoModel.objects.all())
    assert qs.first().demo_related.name == 'related1'
