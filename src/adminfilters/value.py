from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from adminfilters.mixin import MediaDefinitionFilter, SmartFieldListFilter

if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin
    from django.contrib.admin.views.main import ChangeList
    from django.db.models import Field, Model, QuerySet
    from django.http import HttpRequest


class ValueFilter(MediaDefinitionFilter, SmartFieldListFilter):
    template = "adminfilters/value.html"
    toggleable = False
    filter_title = None
    lookup_name = "exact"
    button = True
    can_negate = True
    negated = False

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: Model,
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.lookup_kwarg = None
        self.lookup_kwarg_negated = None
        self.field_path = field_path
        self.parameters = {}
        self.filters = {}
        for p in self.expected_parameters():
            if p in params:
                self.parameters[p] = params.pop(p)

        super().__init__(field, request, params, model, model_admin, field_path)
        self._params = self.parameters
        self.title = self._get_title()

    def expected_parameters(self) -> list[str | None]:
        self.lookup_kwarg = f"{self.field_path}__{self.lookup_name}"
        self.lookup_kwarg_negated = f"{self.lookup_kwarg}__negate"
        return [self.lookup_kwarg, self.lookup_kwarg_negated]

    def value(self) -> tuple[str, bool]:
        return (
            self.get_parameters(self.lookup_kwarg),
            self.get_parameters(self.lookup_kwarg_negated) == "true",
        )

    def js_options(self) -> str:
        return json.dumps({"button": self.button, "canNegate": self.can_negate, "negated": self.negated})

    def _get_title(self) -> str:
        if self.filter_title:
            return self.filter_title
        if "__" in self.field_path:
            return self.field_path.replace("__", "->")
        return getattr(self.field, "verbose_name", self.field_path)

    @classmethod
    def factory(cls, *, title: str | None = None, lookup_name: str = "exact", **kwargs: Any) -> type:
        kwargs["filter_title"] = title
        kwargs["lookup_name"] = lookup_name
        return type("ValueFilter", (cls,), kwargs)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet[Model]:
        target, exclude = self.value()
        if target:
            try:
                self.filters = {self.lookup_kwarg: target}
                queryset = queryset.exclude(**self.filters) if exclude else queryset.filter(**self.filters)
                """
                if exclude:
                    queryset = queryset.exclude(**self.filters)
                else:
                    queryset = queryset.filter(**self.filters)
                """
            except Exception as e:  # noqa: BLE001
                msg = _("%s filter ignored due to an error %s") % (self.title, e)
                self.model_admin.message_user(request, msg, messages.ERROR)
        return queryset

    def choices(self, changelist: ChangeList) -> list:
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    @property
    def media(self) -> forms.Media:
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (f"admin/js/vendor/select2/i18n/{i18n_name}.js",) if i18n_name else ()
        return forms.Media(
            js=(
                f"admin/js/vendor/jquery/jquery{extra}.js",
                *i18n_file,
                "admin/js/jquery.init.js",
                f"adminfilters/value{extra}.js",
            ),
            css={
                "screen": ("adminfilters/adminfilters.css",),
            },
        )


class MultiValueFilter(ValueFilter):
    template: str = "adminfilters/value_multi.html"
    separator: str = ","
    filter_title: str = ""
    lookup_name: str = "in"

    def placeholder(self) -> str:  # noqa: PLR6301
        return _("comma separated list of values")

    def value(self) -> list[str]:
        values = self.get_parameters(self.lookup_kwarg, None, multi=True)
        return [values, self.get_parameters(self.lookup_kwarg_negated, "") == "true"]


TextFieldFilter = ValueFilter
ForeignKeyFieldFilter = TextFieldFilter
MultiValueTextFieldFilter = MultiValueFilter
