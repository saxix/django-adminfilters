from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from django.contrib.admin.utils import prepare_lookup_value
from django.db.models.fields import AutoField, BigAutoField, Field, IntegerField
from django.utils.translation import gettext_lazy as _

from adminfilters.mixin import SmartFieldListFilter

if TYPE_CHECKING:
    from collections.abc import Generator

    from django.contrib.admin import ModelAdmin
    from django.contrib.admin.views.main import ChangeList
    from django.db.models import Model, QuerySet
    from django.http import HttpRequest


class MultipleSelectFieldListFilter(SmartFieldListFilter):
    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: Model,
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.lookup_kwarg = f"{field_path}_filter"
        self.filter_statement = f"{field_path}"

        self._params = params
        self.lookup_val = self.get_parameters(self.lookup_kwarg, pop=True)

        self.lookup_choices = field.get_choices(include_blank=False)
        super().__init__(field, request, params, model, model_admin, field_path)
        self.used_parameters[self.lookup_kwarg] = prepare_lookup_value(self.lookup_kwarg, self.lookup_val)

    def expected_parameters(self) -> list[str | None]:
        return [self.lookup_kwarg]

    def get_field(self) -> Field:
        return self.field.remote_field.model._meta.pk

    def values(self) -> list[str]:
        """
        Returns a list of values to filter on.
        """
        values = []
        value = self.used_parameters.get(self.lookup_kwarg, None)
        if value:
            values = value.split(",")

        field = self.get_field()
        # convert to integers if IntegerField
        if type(field) in {IntegerField, AutoField, BigAutoField}:
            values = [int(x) for x in values]
        return values

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> NoReturn:
        raise NotImplementedError

    def choices(self, cl: ChangeList) -> Generator[dict[str, str | bool], None, None]:
        yield {
            "selected": self.lookup_val is None,
            "query_string": cl.get_query_string({}, [self.lookup_kwarg]),
            "display": _("All"),
        }
        for pk_val, val in self.lookup_choices:
            selected = pk_val in self.values()
            pk_list = set(self.values())
            if selected:
                pk_list.remove(pk_val)
            else:
                pk_list.add(pk_val)
            queryset_value = ",".join([str(x) for x in pk_list])
            if pk_list:
                query_string = cl.get_query_string({
                    self.lookup_kwarg: queryset_value,
                })
            else:
                query_string = cl.get_query_string({}, [self.lookup_kwarg])
            yield {
                "selected": selected,
                "query_string": query_string,
                "display": val,
            }


class IntersectionFieldListFilter(MultipleSelectFieldListFilter):
    """
    A FieldListFilter which allows multiple selection of
    filters for many-to-many type fields. A list of objects will be
    returned whose m2m contains all the selected filters.
    """

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:  # noqa: ARG002
        for value in self.values():
            filter_dct = {self.filter_statement: value}
            queryset = queryset.filter(**filter_dct)
        return queryset


class UnionFieldListFilter(MultipleSelectFieldListFilter):
    """
    A FieldListFilter which allows multiple selection of
    filters for many-to-many type fields, or any type with choices.
    A list of objects will be returned whose m2m or value set
    contains one of the selected filters.
    """

    def get_field(self) -> Field:
        try:
            field = super().get_field()
        except AttributeError as e:  # pragma: no cover
            if hasattr(self.field, "choices") and self.field.choices:
                field = self.field  # It's a *Field with choices
            else:
                raise AttributeError("Multiselect field must be a FK or any type with choices") from e
        return field

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:  # noqa: ARG002
        filter_values = self.values()
        if filter_values:
            filter_statement = f"{self.filter_statement}__in"
            filter_dct = {filter_statement: filter_values}
            queryset = queryset.filter(**filter_dct).distinct()
        return queryset
