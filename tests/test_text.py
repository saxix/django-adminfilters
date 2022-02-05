import pytest
from demo.models import DemoModel, DemoRelated

from adminfilters.filters import MultiValueFilter, ValueFilter


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
    assert ValueFilter.factory(title="Title")(None, None, {}, None, None, "unique").media


@pytest.mark.parametrize("value,negate,expected", [("n", False, []),
                                                   ("a1", False, ["a1"]),
                                                   ("a1", True, ['a2', 'b1', 'c1']),
                                                   ])
def test_TextFieldFilter(fixtures, value, negate, expected):
    f = ValueFilter(DemoModel._meta.get_field('name'), None,
                    {"name": value, "name__negate": str(negate).lower()}, None, None, 'name')

    result = f.queryset(None, DemoModel.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected


def test_factory(fixtures):
    F = ValueFilter.factory(title="CustomTitle")
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
    f = MultiValueFilter(DemoModel._meta.get_field('name'), None,
                         {"name__in": value, "name__in__negate": str(negate).lower()}, None, None, 'name')
    result = f.queryset(None, DemoModel.objects.all())
    value = list(result.values_list("name", flat=True))
    assert value == expected
