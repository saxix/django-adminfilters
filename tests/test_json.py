import pytest
from demoproject.demoapp.models import DemoModel, DemoRelated

from adminfilters.json import JsonFieldFilter
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
    # DemoModelField.objects.create(char="a1", unique=1, **DATA)
    related1 = DemoRelated.objects.create(name='related1')
    related2 = DemoRelated.objects.create(name='related2')
    related3 = DemoRelated.objects.create(name='related3')
    DemoModel.objects.create(name="name1", demo_related=related1, flags={"v": 1})
    DemoModel.objects.create(name="name1.1", demo_related=related1, flags={"v": 1})
    DemoModel.objects.create(name="name2", demo_related=related2, flags={"v": 2})
    DemoModel.objects.create(name="name2.2", demo_related=related2, flags={"v": '2'})
    DemoModel.objects.create(name="nameNone", demo_related=related3, flags={})

    # DemoModelField.objects.create(char="a2", unique=2, **DATA)
    # DemoModelField.objects.create(char="b1", unique=3, **DATA)


def test_media():
    assert GenericLookupFieldFilter.factory('char')(None, {}, None, None).media


def test_JsonFieldFilter(fixtures):
    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "1",
                                       "flags__negate": "false", "flags__options": "e"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    assert list(result.values_list("flags__v", flat=True)) == [1, 1]

    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "1",
                                       "flags__negate": "false", "flags__options": "i"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    assert list(result.values_list("flags__v", flat=True)) == [1, 1, None]
    # negate
    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "1",
                                       "flags__negate": "true",
                                       "flags__options": "e"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    # this is a Django bug. It should returns [2, "2"]
    assert list(result.values_list("flags__v", flat=True)) == [2, 2]

    # negate / include
    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "1",
                                       "flags__negate": "true",
                                       "flags__options": "i"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    # this is a Django bug. It should returns [2, "2"]
    assert list(result.values_list("flags__v", flat=True)) == [2, 2, None]

    # cast to int
    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "2",
                                       "flags__negate": "false",
                                       "flags__type": "num",
                                       "flags__options": "e"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    assert list(result.values_list("flags__v", flat=True)) == [2]

    # cast to char
    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "2",
                                       "flags__negate": "false",
                                       "flags__type": "str",
                                       "flags__options": "e"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    assert list(result.values_list("flags__v", flat=True)) == [2]

    # cast to char/include
    f = JsonFieldFilter('json', None, {"flags__key": "v",
                                       "flags__value": "2",
                                       "flags__negate": "false",
                                       "flags__type": "str",
                                       "flags__options": "i"}, None, None, 'flags')
    result = f.queryset(None, DemoModel.objects.all())
    assert list(result.values_list("flags__v", flat=True)) == [2, None]
