from django.contrib.admin.filters import (AllValuesFieldListFilter,
                                          BooleanFieldListFilter,
                                          ChoicesFieldListFilter,
                                          RelatedFieldListFilter,)


class AllValuesComboFilter(AllValuesFieldListFilter):
    template = 'adminfilters/combobox.html'


class AllValuesRadioFilter(AllValuesFieldListFilter):
    template = 'adminfilters/dradio.html'


class RelatedFieldComboFilter(RelatedFieldListFilter):
    template = 'adminfilters/combobox.html'


class RelatedFieldRadioFilter(RelatedFieldListFilter):
    template = 'adminfilters/radio.html'


class ChoicesFieldComboFilter(ChoicesFieldListFilter):
    template = 'adminfilters/combobox.html'


class ChoicesFieldRadioFilter(ChoicesFieldListFilter):
    template = 'adminfilters/radio.html'


class BooleanRadioFilter(BooleanFieldListFilter):
    template = 'adminfilters/radio.html'
