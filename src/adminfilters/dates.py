import re

from django.contrib.admin.options import IncorrectLookupParameters
from django.db.models import DateField, DateTimeField

from adminfilters.numbers import NumberFilter


class DateRangeFilter(NumberFilter):
    rex1 = re.compile(r"^(>=|<=|>|<|=)?(\d{4}-\d{2}-\d{2})$")
    re_range = re.compile(r"^(\d{4}-\d{2}-\d{2})..(\d{4}-\d{2}-\d{2})$")
    re_list = re.compile(r"(\d{4}-\d{2}-\d{2}),?")
    re_unlike = re.compile(r"^(<>)(?P<date>\d{4}-\d{2}-\d{2})$")

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if isinstance(field, DateTimeField):
            self.extra_lookup = "__date"
        elif isinstance(field, DateField):
            self.extra_lookup = ""

    def queryset(self, request, queryset):
        if self.value() and self.value()[0]:
            raw_value = self.value()[0]
            m1 = self.rex1.match(raw_value)
            m_range = self.re_range.match(raw_value)
            m_list = self.re_list.match(raw_value)
            m_unlike = self.re_unlike.match(raw_value)
            lk = f"{self.field.name}{self.extra_lookup}"
            if m_unlike and m_unlike.groups():
                match = f"{lk}__exact"
                op, value = self.re_unlike.match(raw_value).groups()
                queryset = queryset.exclude(**{match: value})
            else:
                if m1 and m1.groups():
                    op, value = self.rex1.match(raw_value).groups()
                    match = f"{lk}__{self.map[op or '=']}"
                    self.filters = {match: value}
                elif m_range and m_range.groups():
                    start, end = self.re_range.match(raw_value).groups()
                    self.filters = {f"{lk}__gte": start, f"{lk}__lte": end}
                elif m_list and m_list.groups():
                    value = raw_value.split(",")
                    match = f"{lk}__in"
                    self.filters = {match: value}
                else:  # pragma: no cover
                    raise IncorrectLookupParameters()

                try:
                    queryset = queryset.filter(**self.filters)
                except Exception:
                    raise IncorrectLookupParameters(self.value())
        return queryset
