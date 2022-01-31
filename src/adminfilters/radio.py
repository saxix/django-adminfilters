from django.contrib.admin.filters import (AllValuesFieldListFilter,
                                          BooleanFieldListFilter,
                                          ChoicesFieldListFilter,
                                          RelatedFieldListFilter,)


class AllValuesRadioFilter(AllValuesFieldListFilter):
    template = 'adminfilters/fieldradio.html'


class RelatedFieldRadioFilter(RelatedFieldListFilter):
    template = 'adminfilters/fieldradio.html'


class ChoicesFieldRadioFilter(ChoicesFieldListFilter):
    template = 'adminfilters/fieldradio.html'


class BooleanRadioFilter(BooleanFieldListFilter):
    template = 'adminfilters/fieldradio.html'
