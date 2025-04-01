from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    BooleanFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
)

from .mixin import WrapperMixin


class AllValuesRadioFilter(WrapperMixin, AllValuesFieldListFilter):
    template = "adminfilters/radio.html"


class RelatedFieldRadioFilter(WrapperMixin, RelatedFieldListFilter):
    template = "adminfilters/radio.html"


class ChoicesFieldRadioFilter(WrapperMixin, ChoicesFieldListFilter):
    template = "adminfilters/radio.html"


class BooleanRadioFilter(WrapperMixin, BooleanFieldListFilter):
    template = "adminfilters/radio.html"
