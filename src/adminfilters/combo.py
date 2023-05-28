from django.contrib.admin.filters import AllValuesFieldListFilter, ChoicesFieldListFilter, RelatedFieldListFilter

from .mixin import WrappperMixin


class AllValuesComboFilter(WrappperMixin, AllValuesFieldListFilter):
    template = "adminfilters/combobox.html"


class RelatedFieldComboFilter(WrappperMixin, RelatedFieldListFilter):
    template = "adminfilters/combobox.html"


class ChoicesFieldComboFilter(WrappperMixin, ChoicesFieldListFilter):
    template = "adminfilters/combobox.html"
