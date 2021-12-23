from demoproject.demoapp.models import DemoModel2, DemoRelated

from adminfilters.autocomplete import get_real_field


def test_get_real_field():
    f = get_real_field(DemoModel2, 'demo_items__demo_related__name')
    assert f.name == 'name'
    assert f.model == DemoRelated
