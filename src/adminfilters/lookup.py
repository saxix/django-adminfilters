from django import forms
from django.conf import settings
from django.contrib.admin import FieldListFilter, SimpleListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language
from django.utils.translation import gettext as _


class GenericLookupFieldFilter(SimpleListFilter):
    template = 'adminfilters/text.html'

    prefixes = None
    # lookup_val = 'field|filter'
    parameter_name = None

    @classmethod
    def factory(cls, lookup, title=None):
        if title is None:
            title = lookup.replace('__', '->')
        parts = lookup.split('__')
        if len(parts) == 1:
            lookup = '%s__iexact' % parts[0]
        elif len(parts) < 2:
            raise Exception(
                "lookup must contains at least two parts. ForeignKey|Field|Filter (groups|name|istartswith)")

        return type('TextFieldFilter',
                    (cls,), {'parameter_name': lookup.replace('__', '|'),
                             'title': title})

    @property
    def title(self):
        # getattr(field, 'verbose_name', field_path)
        return '--'

    def has_output(self):
        return True

    def value(self):
        return self.used_parameters.get(self.parameter_name, '')

    def queryset(self, request, queryset):
        if self.value():
            field = self.parameter_name.replace('|', '__')
            return queryset.filter(**{field: self.value()})
        return queryset

    def lookups(self, request, model_admin):
        return []

    def choices(self, changelist):
        yield {
            'selected': False,
            'query_string': changelist.get_query_string(
                {},
                [self.parameter_name, ]
            ),
            'lookup_kwarg': self.parameter_name,
            'display': _('All'),
            'value': self.value(),
        }
