import json

import pytest

from adminfilters.checkbox import RelatedFieldCheckBoxFilter
from adminfilters.json import JsonFieldFilter
from adminfilters.lookup import GenericLookupFieldFilter
from adminfilters.numbers import NumberFilter
from demoproject.demoapp.models import DemoModel, DemoModelField, DemoRelated

from adminfilters.filters import ForeignKeyFieldFilter, TextFieldFilter

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
    "choices": 2,
    "flags": {},
}


@pytest.fixture
def fixtures(db):
    for i in range(1, 5):
        values = DATA.copy()
        values['unique'] = i
        DemoModelField.objects.create(**values)


@pytest.mark.parametrize("op,expected", [("=1", "1"),
                                         ("1", "1"),
                                         (">1", "2,3,4"),
                                         (">=1", "1,2,3,4"),
                                         ("<>2", "1,3,4"),
                                         ("<2", "1"),
                                         ("<=2", "1,2"),
                                         ("1,3", "1,3"),
                                         ("2..4", "2,3,4"),
                                         ])
def test_JsonFieldFilter(fixtures, op, expected):
    f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": op}, None, None, 'unique')
    result = f.queryset(None, DemoModelField.objects.all())
    value = list(result.values_list("unique", flat=True))
    assert value == expected.split(","), value
    #
    # f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": "=1"}, None, None, 'unique')
    # result = f.queryset(None, DemoModelField.objects.all())
    # assert list(result.values_list("unique", flat=True)) == ['1']
    #
    # f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": ">1"}, None, None, 'unique')
    # result = f.queryset(None, DemoModelField.objects.all())
    # assert list(result.values_list("unique", flat=True)) == ['2', '3', '4']
    #
    # f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": "<3"}, None, None, 'unique')
    # result = f.queryset(None, DemoModelField.objects.all())
    # assert list(result.values_list("unique", flat=True)) == ['0', '1', '2']
    #
    # f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": "<>3"}, None, None, 'unique')
    # result = f.queryset(None, DemoModelField.objects.all())
    # assert list(result.values_list("unique", flat=True)) == ['0', '1', '2']
    #
    # f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": ">=4"}, None, None, 'unique')
    # result = f.queryset(None, DemoModelField.objects.all())
    # assert list(result.values_list("unique", flat=True)) == ['0', '1', '2']
    #
    # f = NumberFilter(DemoModelField._meta.get_field('unique'), None, {"unique": "<=2"}, None, None, 'unique')
    # result = f.queryset(None, DemoModelField.objects.all())
    # assert list(result.values_list("unique", flat=True)) == ['0', '1', '2']
