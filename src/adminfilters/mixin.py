from typing import Any

from django import forms
from django.contrib.admin import AdminSite, FieldListFilter, ListFilter
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Field, Model, QuerySet
from django.http import HttpRequest

from adminfilters.compat import DJANGO_5


class WrapperMixin:
    negated: bool = False
    can_negate: bool = False
    title: str = ""
    negated_title: str = ""
    placeholder: str = ""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.error = None
        self.error_message = None
        super().__init__(*args, **kwargs)
        if hasattr(self, "media") and self.model_admin and not isinstance(self.model_admin, AdminFiltersMixin):
            raise AttributeError(f"{self.model_admin.__class__.__name__} must inherit from AdminFiltersMixin")

    def get_parameters(
        self, param_name: str, default: str = "", multi: bool = False, pop: bool = False, separator: str = ","
    ) -> str:
        val = self._params.pop(param_name, default) if pop else self._params.get(param_name, default)
        if val:
            if DJANGO_5:
                if isinstance(val, list) and not multi:
                    val = val[-1]
            elif multi:
                val = val.split(separator)
        return val

    def html_attrs(self) -> dict[str, str]:
        classes = f"adminfilters box {self.__class__.__name__.lower()}"
        if self.error_message:
            classes += " error"

        return {
            "class": classes,
            "id": "_".join(self.expected_parameters()),
        }

    def get_title(self) -> str:
        if not self.can_negate and self.negated:
            if self.negated_title:
                return self.negated_title
            return f"not {self.title}"
        return self.title


class SmartListFilter(WrapperMixin, ListFilter):
    def __init__(self, request: HttpRequest, params: dict[str, str], model: Model, model_admin: ModelAdmin) -> None:
        self.model_admin = model_admin
        self._params = params
        super().__init__(request, params, model, model_admin)


class SmartFieldListFilter(WrapperMixin, FieldListFilter):
    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: Model,
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.model_admin = model_admin
        self._params = params.copy()
        super().__init__(field, request, params, model, model_admin, field_path)


class MediaDefinitionFilter:
    pass


class AdminFiltersMixin(ModelAdmin):
    def _check_linked_fields_modeladmin(self) -> list[checks.Error]:  # noqa: C901
        from .autocomplete import LinkedAutoCompleteFilter  # noqa: PLC0415

        linked_filters = [
            e for e in self.list_filter if isinstance(e, (list, tuple)) and issubclass(e[1], LinkedAutoCompleteFilter)
        ]
        errs = []
        seen = []
        for entry in linked_filters:
            if entry[1] and entry[1].parent:
                parts = entry[1].parent.split("__")
                m = self.model
                for part in parts:
                    try:
                        m = m._meta.get_field(part).remote_field.model
                    except FieldDoesNotExist as e:  # noqa: PERF203
                        errs.append(
                            checks.Error(
                                f"{m}` {e}",
                                obj=self,
                                id="adminfilters.E001",
                            )
                        )
                    else:
                        try:
                            ma: ModelAdmin = self.admin_site._registry[m]
                        except KeyError:
                            for proxy in m.__subclasses__():
                                if proxy in self.admin_site._registry:
                                    ma = self.admin_site._registry[proxy]
                                    break
                            else:
                                errs.append(
                                    checks.Error(
                                        f"{m}` is not registered in {self.admin_site}",
                                        obj=self,
                                        id="adminfilters.E002",
                                    )
                                )
                        else:
                            if ma not in seen and not isinstance(ma, AdminAutoCompleteSearchMixin):
                                errs.append(
                                    checks.Error(
                                        f"{ma}` must inherits from AdminAutoCompleteSearchMixin",
                                        obj=ma.__class__,
                                        id="adminfilters.E003",
                                    )
                                )
                                seen.append(ma)

        return errs

    def _check_linked_fields_order(self) -> list[checks.Error]:
        from .autocomplete import LinkedAutoCompleteFilter  # noqa: PLC0415

        linked_filters = [
            e for e in self.list_filter if isinstance(e, (list, tuple)) and issubclass(e[1], LinkedAutoCompleteFilter)
        ]
        errs = []
        seen = []
        for entry in linked_filters:
            if entry[1] and entry[1].parent and entry[1].parent not in seen:
                errs.append(
                    checks.Error(
                        f"Invalid Filters ordering. '{entry[1].parent}' must be defined before '{entry[0]}'.",
                        obj=self.__class__,
                        id="admin.E040",
                    )
                )
            seen.append(entry[0])
        return errs

    def check(self, **kwargs: Any) -> list[checks.Error]:
        return [
            *super().check(**kwargs),
            *self._check_linked_fields_order(),
            *self._check_linked_fields_modeladmin(),
        ]

    def get_changelist_instance(self, request: HttpRequest) -> ChangeList:
        cl = super().get_changelist_instance(request)
        for flt in cl.filter_specs:
            if hasattr(flt, "media"):
                self.admin_filters_media += flt.media
        return cl

    def __init__(self, model: Model, admin_site: AdminSite) -> None:
        self.admin_filters_media = forms.Media()
        super().__init__(model, admin_site)

    @property
    def media(self) -> forms.Media:
        original = super().media
        if hasattr(self, "admin_filters_media"):
            original += self.admin_filters_media
        return original


class AdminAutoCompleteSearchMixin(ModelAdmin):
    def get_search_results(self, request: HttpRequest, queryset: QuerySet, search_term: str) -> tuple[QuerySet, bool]:
        field_names = [f.name for f in self.model._meta.get_fields()]
        filters = {k: v for k, v in request.GET.items() if k in field_names}
        queryset = queryset.filter(**filters)
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        return queryset, may_have_duplicates
