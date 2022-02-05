import pytest
from demo.models import DemoModel, DemoModelField, DemoRelated

from adminfilters.lookup import GenericLookupFieldFilter



@pytest.fixture
def fixtures(db):
    from demo.utils import DATA
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
