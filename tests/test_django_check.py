from unittest.mock import patch

from demo.models import Country
from django.contrib.admin import ModelAdmin, site

from adminfilters.checks import check_adminfilters_media
from adminfilters.querystring import QueryStringFilter
from adminfilters.text import ValueFilter


def test():
    ret = check_adminfilters_media(None)
    assert ret == []


class BrokenCountryModelAdmin(ModelAdmin):
    list_filter = (
        QueryStringFilter,
        ('name', ValueFilter),)


def test_error():
    with patch.dict(site._registry, {Country: BrokenCountryModelAdmin}, clear=True):
        ret = check_adminfilters_media(None)
        assert len(ret) == 1
