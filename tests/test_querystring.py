import pytest
from demo.models import DemoModelField

from adminfilters.querystring import QueryStringFilter


@pytest.fixture
def fixtures(db):
    from demo.utils import DATA
    for i in range(1, 5):
        values = DATA.copy()
        values['unique'] = i
        DemoModelField.objects.create(**values)


@pytest.mark.parametrize('op,expected', [('unique=1', '1'),
                                         ('unique__in=1,2,3', '1,2,3'),
                                         ('!unique=2', '1,3,4'),
                                         ])
def test_QueryStringFilter(fixtures, op, expected):
    f = QueryStringFilter(None, {'qs': op}, None, None)
    result = f.queryset(None, DemoModelField.objects.all())
    value = list(result.values_list('unique', flat=True))
    assert value == expected.split(','), value
