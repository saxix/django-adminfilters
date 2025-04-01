from collections.abc import Iterable
from typing import Any

from django import forms
from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.db.models import Field, Model, Q, QuerySet
from django.forms import Media
from django.http import HttpRequest
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from .mixin import MediaDefinitionFilter, SmartFieldListFilter


class JsonFieldFilter(MediaDefinitionFilter, SmartFieldListFilter):
    parameter_name = None
    title = None
    template = "adminfilters/json.html"
    can_negate = True
    negated = False
    options = True
    key_placeholder = _("JSON key")
    placeholder = _("JSON value")

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: Model,
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.lookup_kwarg_key = f"{field_path}__key"
        self.lookup_kwarg_value = f"{field_path}__value"
        self.lookup_kwarg_negated = f"{field_path}__negate"
        self.lookup_kwarg_options = f"{field_path}__options"
        self.lookup_kwarg_type = f"{field_path}__type"

        self.field = field
        self.query_string = None
        self.field_path = field_path
        self.title = getattr(field, "verbose_name", field_path)
        super().__init__(field, request, params, model, model_admin, field_path)

        self.lookup_key_val = self.get_parameters(self.lookup_kwarg_key, "")
        self.lookup_value_val = self.get_parameters(self.lookup_kwarg_value, "")
        self.lookup_negated_val = self.get_parameters(self.lookup_kwarg_negated, "false")
        self.lookup_type_val = self.get_parameters(self.lookup_kwarg_type, "any")
        self.lookup_options_val = self.get_parameters(self.lookup_kwarg_options, "e")

    @classmethod
    def factory(cls, **kwargs: Any) -> "type":
        return type("JsonFieldFilter", (cls,), kwargs)

    def expected_parameters(self) -> Iterable[str]:
        return [
            self.lookup_kwarg_key,
            self.lookup_kwarg_value,
            self.lookup_kwarg_negated,
            self.lookup_kwarg_options,
            self.lookup_kwarg_type,
        ]

    def value(self) -> list[str]:
        return [
            self.lookup_key_val,
            self.lookup_value_val,
            self.lookup_options_val,
            (self.can_negate and self.lookup_negated_val == "true") or self.negated,
            self.lookup_type_val,
        ]

    def choices(self, changelist: ChangeList) -> list:
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:  # noqa: ARG002
        key, value, options, negated, type_ = self.value()
        if key:
            if type_ == "any" and value.isnumeric():
                filters = Q(**{f"{self.field_path}__{key}": value}) | Q(**{f"{self.field_path}__{key}": int(value)})
            elif type_ == "num" and value.isnumeric():
                filters = Q(**{f"{self.field_path}__{key}": float(value)})
            else:  # type_ == 'str':
                filters = Q(**{f"{self.field_path}__{key}": str(value)})

            if negated:
                if self.options and options == "e":
                    filters = ~filters
                else:
                    filters = Q(**{f"{self.field_path}__{key}__isnull": True}) | ~filters
            elif options == "i":
                filters |= Q(**{f"{self.field_path}__{key}__isnull": True})

            queryset = queryset.filter(filters)
        return queryset

    @property
    def media(self) -> Media:
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (f"admin/js/vendor/select2/i18n/{i18n_name}.js",) if i18n_name else ()
        return forms.Media(
            js=(
                f"admin/js/vendor/jquery/jquery{extra}.js",
                *i18n_file,
                "admin/js/jquery.init.js",
                f"adminfilters/jsonfilter{extra}.js",
            ),
            css={
                "screen": ("adminfilters/adminfilters.css",),
            },
        )
