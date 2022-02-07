import pytest
from demo.models import DemoModelField

from adminfilters.querystring import QueryStringFilter


@pytest.fixture
def fixtures(db):
    from demo.utils import DATA
    for i in range(1, 5):
        values = DATA.copy()
        values['unique'] = i
        values['logic'] = bool(i % 2)
        DemoModelField.objects.create(**values)


@pytest.mark.parametrize('op,expected,error', [('unique=1', '1', None),
                                               ('unique__in=1,2,3', '1,2,3', None),
                                               ('!unique=2', '1,3,4', None),
                                               ('logic=_T_', '1,3', None),
                                               ('logic=_F_', '2,4', None),
                                               ('!logic=_F_', '1,3', None),
                                               ('wrong=1', '1,2,3,4', "Unknown field or lookup: 'wrong'"),
                                               ('logic_x=1', '1,2,3,4', "Unknown field or lookup: 'logic_x'"),
                                               ])
def test_QueryStringFilter(fixtures, op, expected, error):
    f = QueryStringFilter(None, {'qs': op}, None, None)
    result = f.queryset(None, DemoModelField.objects.all())
    value = list(result.values_list('unique', flat=True))
    assert value == expected.split(','), value
    assert f.error_message == error


def test_media():
    assert QueryStringFilter.factory(title='Title')(None, {}, None, 'unique').media
