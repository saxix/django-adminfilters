import re

from django.contrib.admin import FieldListFilter
from django.contrib.admin.options import IncorrectLookupParameters
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


class NumberFilter(FieldListFilter):
    template = 'adminfilters/text.html'

    rex1 = re.compile(r'^(>=|<=|>|<|=)?([-+]?[0-9]+)$')
    rex2 = re.compile(r'^(\d+)..(\d+)$')
    rex3 = re.compile(r'(\d+),?')
    rex4 = re.compile(r'^(<>)?([-+]?[0-9]+)$')
    # rex5 = re.compile(r'^(\d+)..(\d+)$')
    map = {">=": "gte",
           "<=": "lte",
           ">": "gt",
           "<": "lt",
           "=": "exact",
           "<>": "not",
           }

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = mark_safe(f'{self.title} <small>(use >,>=,<,<=, fixed, list)</small>')

    def choices(self, changelist):
        yield {
            'selected': False,
            'query_string': changelist.get_query_string(
                {},
                [self.field.name, ]
            ),
            'lookup_kwarg': self.field.name,
            'display': _('All'),
            'value': self.value(),
        }

    def value(self):
        return self.used_parameters.get(self.field.name, '')

    def expected_parameters(self):
        return [self.field.name]

    def queryset(self, request, queryset):
        if self.value():
            raw = self.value()
            m1 = self.rex1.match(raw)
            m2 = self.rex2.match(raw)
            m3 = self.rex3.match(raw)
            m4 = self.rex4.match(raw)
            if m1 and m1.groups():
                op, value = self.rex1.match(raw).groups()
                match = "%s__%s" % (self.field.name, self.map[op or '='])
                queryset = queryset.filter(**{match: value})
            elif m2 and m2.groups():
                start, end = self.rex2.match(raw).groups()
                queryset = queryset.filter(**{f"{self.field.name}__gte": start,
                                              f"{self.field.name}__lte": end})
            elif m3 and m3.groups():
                value = raw.split(',')
                match = "%s__in" % self.field.name
                queryset = queryset.filter(**{match: value})
            # elif m3 and m3.groups():
            #     match = "%s__exact" % self.field.name
            #     queryset = queryset.filter(**{match: raw})
            elif m4 and m4.groups():
                match = "%s__exact" % self.field.name
                op, value = self.rex4.match(raw).groups()
                queryset = queryset.exclude(**{match: value})
            else:  # pragma: no cover
                raise IncorrectLookupParameters()
        return queryset


# backward compatibility
MaxMinFilter = NumberFilter

