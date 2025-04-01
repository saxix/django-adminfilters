from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, ClassVar

from django.contrib.admin.options import IncorrectLookupParameters

from .value import ValueFilter

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


class NumberFilter(ValueFilter):
    rex1 = re.compile(r"^(>=|<=|>|<|=)?([-+]?[0-9]+)$")
    re_range = re.compile(r"^(\d+)\.{2,}(\d+)$")
    re_list = re.compile(r"(\d+),?")
    re_unlike = re.compile(r"^(<>)([-+]?[0-9]+)$")
    map: ClassVar[dict[str, str]] = {
        ">=": "gte",
        "<=": "lte",
        ">": "gt",
        "<": "lt",
        "=": "exact",
        "<>": "not",
    }
    can_negate = False

    @classmethod
    def factory(cls, *, title: str | None = None, **kwargs: Any) -> type:
        if "lookup_name" in kwargs:
            raise ValueError(f"'lookup_name' is not a valid value for '{cls.__class__.__name__}.factory'")
        return super().factory(title=title, **kwargs)

    def placeholder(self) -> str:  # noqa: PLR6301
        return "1 or >< <=> <> 1 or 1..10 or 1,4,5"

    def expected_parameters(self) -> list[str | None]:
        self.lookup_kwarg = self.field_path
        return [self.lookup_kwarg]

    def value(self) -> list[str]:
        return [
            self.get_parameters(self.lookup_kwarg),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:  # noqa: ARG002
        if self.value() and self.value()[0]:
            raw_value = self.value()[0]
            m1 = self.rex1.match(raw_value)
            m_range = self.re_range.match(raw_value)
            m_list = self.re_list.match(raw_value)
            m_unlike = self.re_unlike.match(raw_value)
            if m_unlike and m_unlike.groups():
                match = f"{self.field_path}__exact"
                op, value = self.re_unlike.match(raw_value).groups()
                queryset = queryset.exclude(**{match: value})
            else:
                if m1 and m1.groups():
                    op, value = self.rex1.match(raw_value).groups()
                    match = "{}__{}".format(self.field_path, self.map[op or "="])
                    self.filters = {match: value}
                elif m_range and m_range.groups():
                    start, end = self.re_range.match(raw_value).groups()
                    self.filters = {
                        f"{self.field_path}__gte": start,
                        f"{self.field_path}__lte": end,
                    }
                elif m_list and m_list.groups():
                    value = raw_value.split(",")
                    match = f"{self.field_path}__in"
                    self.filters = {match: value}
                else:  # pragma: no cover
                    raise IncorrectLookupParameters
                try:
                    queryset = queryset.filter(**self.filters)
                except Exception as e:
                    raise IncorrectLookupParameters(self.value()) from e
        return queryset


# backward compatibility
MaxMinFilter = NumberFilter
