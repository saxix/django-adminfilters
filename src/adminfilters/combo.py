from django.contrib.admin.filters import (AllValuesFieldListFilter,
                                          ChoicesFieldListFilter,
                                          RelatedFieldListFilter,)


class AllValuesComboFilter(AllValuesFieldListFilter):
    template = 'adminfilters/combobox.html'


class RelatedFieldComboFilter(RelatedFieldListFilter):
    template = 'adminfilters/fieldcombobox.html'


class ChoicesFieldComboFilter(ChoicesFieldListFilter):
    template = 'adminfilters/combobox.html'
