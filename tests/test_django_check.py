from unittest.mock import patch

import pytest
from demo.admin import ArtistModelAdmin
from demo.models import Artist, Band
from django.contrib.admin import ModelAdmin, site

from adminfilters.checkbox import RelatedFieldCheckBoxFilter
from adminfilters.checks import check_adminfilters_media
from adminfilters.filters import ValueFilter
from adminfilters.querystring import QueryStringFilter


def test():
    ret = check_adminfilters_media(None)
    assert ret == [], [e.msg for e in ret]


@pytest.mark.parametrize("filter_class", [QueryStringFilter, ("name", ValueFilter)])
def test_check_error(filter_class):
    class InvalidModelAdmin(ModelAdmin):
        list_filter = (
            "active",
            filter_class,
            ("genre", RelatedFieldCheckBoxFilter),
        )

    with patch.dict(
        site._registry, {Artist: ArtistModelAdmin, Band: InvalidModelAdmin}, clear=True
    ):
        ret = check_adminfilters_media(None)
        assert len(ret) == 1, [e.msg for e in ret]
