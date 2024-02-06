import re

from django.contrib.admin.options import IncorrectLookupParameters

from .value import ValueFilter


class NumberFilter(ValueFilter):
    rex1 = re.compile(r"^(>=|<=|>|<|=)?([-+]?[0-9]+)$")
    re_range = re.compile(r"^(\d+)\.{2,}(\d+)$")
    re_list = re.compile(r"(\d+),?")
    re_unlike = re.compile(r"^(<>)([-+]?[0-9]+)$")
    map = {
        ">=": "gte",
        "<=": "lte",
        ">": "gt",
        "<": "lt",
        "=": "exact",
        "<>": "not",
    }
    can_negate = False

    # def __init__(self, field, request, params, model, model_admin, field_path):
    #     super().__init__(field, request, params, model, model_admin, field_path)
    #     self.lookup_kwarg = '%s__%s' % (field_path, self.lookup_name)

    @classmethod
    def factory(cls, *, title=None, **kwargs):
        if "lookup_name" in kwargs:
            raise ValueError(
                f"'lookup_name' is not a valid value for "
                f"'{cls.__class__.__name__}.factory'"
            )
        return super().factory(title=title, **kwargs)

    def placeholder(self):
        return "1 or >< <=> <> 1 or 1..10 or 1,4,5"

    # def parse_query_string(self, params):
    #     self.lookup_val = params.get(self.field.name, '')
    def expected_parameters(self):
        self.lookup_kwarg = self.field_path
        return [self.lookup_kwarg]

    def value(self):
        return [
            self.get_parameters(self.lookup_kwarg),
        ]

    def queryset(self, request, queryset):
        if self.value() and self.value()[0]:
            raw_value = self.value()[0]
            m1 = self.rex1.match(raw_value)
            m_range = self.re_range.match(raw_value)
            m_list = self.re_list.match(raw_value)
            m_unlike = self.re_unlike.match(raw_value)
            if m_unlike and m_unlike.groups():
                match = "%s__exact" % self.field_path
                op, value = self.re_unlike.match(raw_value).groups()
                queryset = queryset.exclude(**{match: value})
            else:
                if m1 and m1.groups():
                    op, value = self.rex1.match(raw_value).groups()
                    match = "%s__%s" % (self.field_path, self.map[op or "="])
                    self.filters = {match: value}
                elif m_range and m_range.groups():
                    start, end = self.re_range.match(raw_value).groups()
                    self.filters = {
                        f"{self.field_path}__gte": start,
                        f"{self.field_path}__lte": end,
                    }
                elif m_list and m_list.groups():
                    value = raw_value.split(",")
                    match = "%s__in" % self.field_path
                    self.filters = {match: value}
                # elif m_unlike and m_unlike.groups():
                #     match = '%s__exact' % self.field.name
                #     op, value = self.re_unlike.match(raw).groups()
                #     queryset = queryset.exclude(**{match: value})
                else:  # pragma: no cover
                    raise IncorrectLookupParameters()
                try:
                    queryset = queryset.filter(**self.filters)
                except Exception:
                    raise IncorrectLookupParameters(self.value())
        return queryset


# backward compatibility
MaxMinFilter = NumberFilter
