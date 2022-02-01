from django.contrib.admin.filters import (AllValuesFieldListFilter,
                                          BooleanFieldListFilter,
                                          ChoicesFieldListFilter,
                                          RelatedFieldListFilter,)
from django.db.models.fields.related import ForeignObjectRel
from django.db.models.query_utils import Q
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _


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
