from unittest.mock import Mock

import pytest
from demo.admin import ArtistModelAdmin
from demo.factories import ArtistFactory
from demo.management.commands.init_demo import sample_data
from demo.models import Artist
from django.contrib.admin import site

from adminfilters.checkbox import RelatedFieldCheckBoxFilter


@pytest.fixture
def fixtures(db):
    ArtistFactory(name="name1", bands=[])
    return sample_data()


def test_RelatedFieldCheckBoxFilte_single(fixtures, rf):
    acdc, geordie = fixtures
    request = rf.get(f"/?bands__id={geordie.id}")
    f = RelatedFieldCheckBoxFilter(
        Artist._meta.get_field("bands"),
        request,
        {},
        None,
        ArtistModelAdmin(Artist, site),
        "bands",
    )
    result = f.queryset(None, Artist.objects.all())

    value = sorted(list(result.values_list("name", flat=True)))
    assert value == ["Brian"]


def test_RelatedFieldCheckBoxFilte_multi(fixtures, rf):
    acdc, geordie = fixtures
    request = rf.get(f"/?bands__id={acdc.id}&bands_id={geordie.id}")
    f = RelatedFieldCheckBoxFilter(
        Artist._meta.get_field("bands"),
        request,
        {},
        None,
        ArtistModelAdmin(Artist, site),
        "bands",
    )
    result = f.queryset(None, Artist.objects.all())

    value = sorted(list(result.values_list("name", flat=True)))
    assert value == ["Angus", "Bon", "Brian", "Malcom", "Phil"]


def test_RelatedFieldCheckBoxFilte_isnull(fixtures, rf):
    request = rf.get("/?bands__isnull=true")
    f = RelatedFieldCheckBoxFilter(
        Artist._meta.get_field("bands"),
        request,
        {"bands__isnull": "true"},
        None,
        ArtistModelAdmin(Artist, site),
        "bands",
    )
    result = f.queryset(None, Artist.objects.all())

    value = sorted(list(result.values_list("name", flat=True)))
    assert value == ["name1"]


def test_RelatedFieldCheckBoxFilte_choices(fixtures, rf):
    request = rf.get("/")
    f = RelatedFieldCheckBoxFilter(
        Artist._meta.get_field("bands"),
        request,
        {},
        None,
        ArtistModelAdmin(Artist, site),
        "bands",
    )
    choices = list(f.choices(Mock()))
    assert len(choices) == 4
    assert [c["display"] for c in choices] == ["All", "None", "AC/DC", "Geordie"]
