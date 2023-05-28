from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    BooleanFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
)

from .mixin import WrappperMixin


class AllValuesRadioFilter(WrappperMixin, AllValuesFieldListFilter):
    template = "adminfilters/radio.html"


class RelatedFieldRadioFilter(WrappperMixin, RelatedFieldListFilter):
    template = "adminfilters/radio.html"


class ChoicesFieldRadioFilter(WrappperMixin, ChoicesFieldListFilter):
    template = "adminfilters/radio.html"


class BooleanRadioFilter(WrappperMixin, BooleanFieldListFilter):
    template = "adminfilters/radio.html"
