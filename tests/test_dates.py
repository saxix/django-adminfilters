import pytest
from demo.models import DemoModelField

from adminfilters.dates import DateRangeFilter


@pytest.fixture
def fixtures(db):
    from demo.utils import DATA

    for i in range(1, 6):
        values = DATA.copy()
        values["unique"] = i
        values["datetime"] = "2000-01-%d 10:30:00-00:00" % i
        values["date"] = "2000-01-%d" % i
        values["json"] = {}

        DemoModelField.objects.create(**values)


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
def test_NumberFilter(fixtures, field, op, expected):
    f = DateRangeFilter(
        DemoModelField._meta.get_field(field), None, {field: op}, None, None, field
    )
    assert f.value() == [op]
    result = f.queryset(None, DemoModelField.objects.all())
    value = [x.strftime("%Y-%m-%d") for x in result.values_list(field, flat=True)]
    assert value == expected.split(","), f.error_message


def test_factory(fixtures):
    assert DateRangeFilter.factory(title="CustomTitle")


def test_factory_invalid(fixtures):
    with pytest.raises(ValueError):
        assert DateRangeFilter.factory(title="CustomTitle", lookup_name="in")
