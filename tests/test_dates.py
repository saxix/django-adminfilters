from datetime import datetime
from unittest.mock import Mock

import pytest
from demo.models import DemoModelField
from django.db.backends.postgresql.psycopg_any import DateRange

from adminfilters.dates import DateFilter, DateInDateRangeFilter
from adminfilters.mixin import AdminFiltersMixin


@pytest.fixture
def fixtures(db):
    from demo.factories import DemoModelFieldFactory
    from demo.utils import DATA

    for i in range(1, 6):
        values = DATA.copy()
        values["unique"] = i
        values["datetime"] = "2000-01-%d 10:30:00-00:00" % i
        values["date"] = "2000-01-%d" % i
        values["json"] = {}
        values["validity"] = DateRange(datetime(2000, i, 1).date(), datetime(2000, i, 20).date())
        DemoModelFieldFactory(**values)


@pytest.mark.parametrize("field", ("date", "datetime"))
@pytest.mark.parametrize(
    "op,expected",
    [
        ("2000-01-01", "2000-01-01"),
        (">2000-01-03", "2000-01-04,2000-01-05"),
        (">=2000-01-03", "2000-01-03,2000-01-04,2000-01-05"),
        ("<2000-01-03", "2000-01-01,2000-01-02"),
        ("<=2000-01-03", "2000-01-01,2000-01-02,2000-01-03"),
        ("2000-01-02..2000-01-04", "2000-01-02,2000-01-03,2000-01-04"),
        ("2000-01-03,2000-01-05", "2000-01-03,2000-01-05"),
        ("<>2000-01-03", "2000-01-01,2000-01-02,2000-01-04,2000-01-05"),
    ],
)
def test_DateFilter(fixtures, field, op, expected):
    f = DateFilter(DemoModelField._meta.get_field(field), None, {field: op}, None, None, field)
    assert f.value() == [op]
    result = f.queryset(None, DemoModelField.objects.all())
    value = [x.strftime("%Y-%m-%d") for x in result.values_list(field, flat=True)]
    assert value == expected.split(","), f.error_message


def test_factory(fixtures):
    assert DateFilter.factory(title="CustomTitle")


def test_factory_invalid(fixtures):
    with pytest.raises(ValueError):
        assert DateFilter.factory(title="CustomTitle", lookup_name="in")


@pytest.mark.parametrize(
    "value,negated,expected",
    [
        ("2000-01-01", "false", 1),
        ("2000-01-10", "false", 1),
        ("2000-02-10", "false", 1),
        ("2000-02-21", "false", 0),
        ("2000-01-01", "true", 4),
        ("2000-01-10", "true", 4),
        ("2000-02-10", "true", 4),
        ("2000-02-21", "true", 5),
    ],
)
def test_DateInDateRangeFilter(fixtures, value, negated, expected):
    f = DateInDateRangeFilter(
        DemoModelField._meta.get_field("validity"),
        None,
        {"validity__contains": value, "validity__contains__negate": negated},
        None,
        Mock(spec=AdminFiltersMixin),
        "validity",
    )
    assert f.value() == (value, negated == "true")
    result = f.queryset(None, DemoModelField.objects.all())
    assert result.count() == expected, list(result.values_list("validity", flat=True))
