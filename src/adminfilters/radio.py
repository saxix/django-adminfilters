from django.contrib.admin.filters import (AllValuesFieldListFilter,
                                          BooleanFieldListFilter,
                                          ChoicesFieldListFilter,
                                          RelatedFieldListFilter,)


class AllValuesRadioFilter(AllValuesFieldListFilter):
    template = 'adminfilters/radio.html'


class RelatedFieldRadioFilter(RelatedFieldListFilter):
    template = 'adminfilters/radio.html'


class ChoicesFieldRadioFilter(ChoicesFieldListFilter):
    template = 'adminfilters/radio.html'


class BooleanRadioFilter(BooleanFieldListFilter):
    template = 'adminfilters/radio.html'
