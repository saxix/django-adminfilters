import pytest
from demoproject.demoapp.models import DemoModel, DemoRelated

from adminfilters.filters import TextFieldFilter
from adminfilters.lookup import GenericLookupFieldFilter
from adminfilters.text import MultiValueTextFieldFilter

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
    related1 = DemoRelated.objects.create(name='related1')
    related2 = DemoRelated.objects.create(name='related2')
    related3 = DemoRelated.objects.create(name='related3')
    DemoModel.objects.create(demo_related=related1, name='a1')
    DemoModel.objects.create(demo_related=related2, name='a2')
    DemoModel.objects.create(demo_related=related3, name='b1')
    DemoModel.objects.create(demo_related=related3, name='c1')


def test_media(fixtures, rf):
    assert GenericLookupFieldFilter.factory('char')(None, {}, None, None).media


@pytest.mark.parametrize("value,negate,expected", [("n", False, []),
                                                   ("a1", False, ["a1"]),
                                                   ("a1", True, ['a2', 'b1', 'c1']),
                                                   ])
def test_TextFieldFilter(fixtures, value, negate, expected):
    f = TextFieldFilter(DemoModel._meta.get_field('name'), None,
                        {"name": value, "name__negate": str(negate).lower()}, None, None, 'name')

    result = f.queryset(None, DemoModel.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected


def test_factory(fixtures):
    F = TextFieldFilter.factory(title="CustomTitle")
    f = F(DemoModel._meta.get_field('name'), None,
          {"name": "a1", "name__negate": "false"}, None, None, 'name')

    result = f.queryset(None, DemoModel.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == ["a1"]


@pytest.mark.parametrize("value,negate,expected", [("n", False, []),
                                                   ("a1", False, ["a1"]),
                                                   ("a1", True, ['a2', 'b1', 'c1']),
                                                   ])
def test_MultiValueTextFieldFilter(fixtures, value, negate, expected):
    f = MultiValueTextFieldFilter(DemoModel._meta.get_field('name'), None,
                                  {"name__in": value, "name__in__negate": str(negate).lower()}, None, None, 'name')
    result = f.queryset(None, DemoModel.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected
