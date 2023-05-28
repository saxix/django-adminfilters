from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import gettext as _


class PermissionPrefixFilter(SimpleListFilter):
    title = "Permission"
    parameter_name = "perm"
    prefixes = (
        ("view", _("View")),
        ("add", _("Add")),
        ("change", _("Change")),
        ("delete", _("Delete")),
        ("--", _("Others")),
    )
    lookup_val = None

    def lookups(self, request, model_admin):
        return self.prefixes

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "--":
            k = [prefix for prefix, label in self.prefixes]
            query = Q()
            for el in k:
                query |= Q(codename__startswith=el)
            return queryset.exclude(query)
        else:
            return queryset.filter(codename__startswith=self.value())
