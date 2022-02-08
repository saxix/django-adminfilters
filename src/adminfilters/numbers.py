import re

from django.contrib.admin.options import IncorrectLookupParameters
from django.utils.safestring import mark_safe

from adminfilters.text import ValueFilter


class NumberFilter(ValueFilter):
    # template = 'adminfilters/text.html'

    rex1 = re.compile(r'^(>=|<=|>|<|=)?([-+]?[0-9]+)$')
    re_range = re.compile(r'^(\d+)\.\.(\d+)$')
    re_list = re.compile(r'(\d+),?')
    re_unlike = re.compile(r'^(<>)([-+]?[0-9]+)$')
    map = {'>=': 'gte',
           '<=': 'lte',
           '>': 'gt',
           '<': 'lt',
           '=': 'exact',
           '<>': 'not',
           }

    # def __init__(self, field, request, params, model, model_admin, field_path):
    #     super().__init__(field, request, params, model, model_admin, field_path)
    # self.title = mark_safe(f'{self.title} <small>(use >,>=,<,<=, fixed, list)</small>')
    # self.lookup_kwarg = field_path

    def _get_title(self):
        return mark_safe(f'{self.title} <small>(use >,>=,<,<=, fixed, list)</small>')

    def value(self):
        return [self.used_parameters.get(self.field.name, '')]

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def queryset(self, request, queryset):
        if self.value() and self.value()[0]:
            raw_value = self.value()[0]
            m1 = self.rex1.match(raw_value)
            m_range = self.re_range.match(raw_value)
            m_list = self.re_list.match(raw_value)
            m_unlike = self.re_unlike.match(raw_value)
            if m_unlike and m_unlike.groups():
                match = '%s__exact' % self.field.name
                op, value = self.re_unlike.match(raw_value).groups()
                queryset = queryset.exclude(**{match: value})
            else:
                if m1 and m1.groups():
                    op, value = self.rex1.match(raw_value).groups()
                    match = '%s__%s' % (self.field.name, self.map[op or '='])
                    self.filters = {match: value}
                elif m_range and m_range.groups():
                    start, end = self.re_range.match(raw_value).groups()
                    self.filters = {f'{self.field.name}__gte': start,
                                    f'{self.field.name}__lte': end}
                elif m_list and m_list.groups():
                    value = raw_value.split(',')
                    match = '%s__in' % self.field.name
                    self.filters = {match: value}
                # elif m_unlike and m_unlike.groups():
                #     match = '%s__exact' % self.field.name
                #     op, value = self.re_unlike.match(raw).groups()
                #     queryset = queryset.exclude(**{match: value})
                else:  # pragma: no cover
                    raise IncorrectLookupParameters()
                queryset = queryset.filter(**self.filters)
        return queryset


# backward compatibility
MaxMinFilter = NumberFilter
