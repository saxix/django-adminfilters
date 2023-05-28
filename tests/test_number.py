import pytest
from demo.models import DemoModelField

from adminfilters.numbers import NumberFilter


@pytest.fixture
def fixtures(db):
    from demo.utils import DATA

    for i in range(1, 5):
        values = DATA.copy()
        values["unique"] = i
        values["json"] = {}
        DemoModelField.objects.create(**values)


@pytest.mark.parametrize(
    "op,expected",
    [
        ("=1", "1"),
        ("1", "1"),
        (">1", "2,3,4"),
        (">=1", "1,2,3,4"),
        ("<>2", "1,3,4"),
        ("<2", "1"),
        ("<=2", "1,2"),
        ("1,3", "1,3"),
        ("2..4", "2,3,4"),
    ],
)
def test_NumberFilter(fixtures, op, expected):
    f = NumberFilter(
        DemoModelField._meta.get_field("unique"),
        None,
        {"unique": op},
        None,
        None,
        "unique",
    )
    assert f.value() == [op]
    result = f.queryset(None, DemoModelField.objects.all())
    value = list(result.values_list("unique", flat=True))
    assert value == expected.split(","), f.error_message


def test_factory(fixtures):
    assert NumberFilter.factory(title="CustomTitle")


def test_factory_invalid(fixtures):
    with pytest.raises(ValueError):
        assert NumberFilter.factory(title="CustomTitle", lookup_name="in")
