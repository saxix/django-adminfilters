from django.contrib.admin.filters import AllValuesFieldListFilter, ChoicesFieldListFilter, RelatedFieldListFilter

from .mixin import WrapperMixin


class AllValuesComboFilter(WrapperMixin, AllValuesFieldListFilter):
    template = "adminfilters/combobox.html"


class RelatedFieldComboFilter(WrapperMixin, RelatedFieldListFilter):
    template = "adminfilters/combobox.html"


class ChoicesFieldComboFilter(WrapperMixin, ChoicesFieldListFilter):
    template = "adminfilters/combobox.html"
