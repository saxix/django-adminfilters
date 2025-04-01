from typing import ClassVar

from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _


class PermissionPrefixFilter(SimpleListFilter):
    title = "Permission"
    parameter_name = "perm"
    prefixes: ClassVar[list[tuple[str, str]]] = [
        ("view", _("View")),
        ("add", _("Add")),
        ("change", _("Change")),
        ("delete", _("Delete")),
        ("--", _("Others")),
    ]
    lookup_val = None

    def lookups(self, request: HttpRequest, model_admin: ModelAdmin) -> list[tuple[str, str]]:  # noqa: ARG002
        return self.prefixes

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:  # noqa: ARG002
        if not self.value():
            return queryset
        if self.value() == "--":
            k = [prefix for prefix, label in self.prefixes]
            query = Q()
            for el in k:
                query |= Q(codename__startswith=el)
            return queryset.exclude(query)
        return queryset.filter(codename__startswith=self.value())
