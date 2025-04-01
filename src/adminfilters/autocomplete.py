from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.forms import Media
from django.urls import reverse
from django.utils.translation import get_language

from .mixin import MediaDefinitionFilter, SmartFieldListFilter

if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin
    from django.contrib.admin.views.main import ChangeList
    from django.db.models import Field, Model
    from django.http import HttpRequest


def get_real_field(model: Model, path: str) -> Field | None:
    parts = path.split("__")
    current = model
    f = None
    for p in parts:
        f = current._meta.get_field(p)
        if f.related_model:
            current = f.related_model
    return f


class AutoCompleteFilter(SmartFieldListFilter, MediaDefinitionFilter):
    template = "adminfilters/autocomplete.html"
    filter_title = None
    parent = None
    parent_lookup_kwarg = None
    ajax_url = None
    css = "adminfilters/adminfilters%s.css"

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: Model,
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.dependants = []
        self.lookup_kwarg = f"{field_path}__exact"
        self.lookup_kwarg_isnull = f"{field_path}__isnull"
        self._params = params
        self.request = request
        self.lookup_val = self.get_parameters(self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)
        self.admin_site = model_admin.admin_site
        self.query_string = ""
        self.target_field = get_real_field(model, field_path)
        self.target_model = self.target_field.related_model
        self.target_opts = self.target_field.model._meta

    def expected_parameters(self) -> list[str]:
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    @property
    def url(self) -> str:
        return self.get_url()

    def get_url(self) -> str:
        if self.ajax_url is None:
            return reverse(f"{self.admin_site.name}:autocomplete")
        return reverse(self.ajax_url)

    def choices(self, changelist: ChangeList) -> list[str]:
        self.query_string = changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull])
        if self.lookup_val:
            get_kwargs = {self.field.target_field.name: self.lookup_val}
            return [str(self.target_model.objects.get(**get_kwargs)) or ""]
        return []

    @property
    def media(self) -> Media:
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (f"admin/js/vendor/select2/i18n/{i18n_name}.js",) if i18n_name else ()
        return Media(
            js=(
                f"admin/js/vendor/jquery/jquery{extra}.js",
                f"admin/js/vendor/select2/select2.full{extra}.js",
                *i18n_file,
                "admin/js/jquery.init.js",
                "admin/js/autocomplete.js",
                f"adminfilters/autocomplete{extra}.js",
            ),
            css={
                "screen": (
                    f"admin/css/vendor/select2/select2{extra}.css",
                    self.css % extra,
                ),
            },
        )

    @classmethod
    def factory(cls, *, title: str | None = None, lookup_name: str = "exact", **kwargs: Any) -> type:
        kwargs["filter_title"] = title
        kwargs["lookup_name"] = lookup_name
        return type("ValueFilter", (cls,), kwargs)

    def get_title(self) -> str:
        if not self.can_negate and self.negated:
            if self.negated_title:
                return self.negated_title
            return f"not {self.title}"
        return self.filter_title or self.title


class LinkedAutoCompleteFilter(AutoCompleteFilter):
    parent = None
    parent_lookup_kwarg = None
    extras: ClassVar[list] = []
    dependants: ClassVar[list[str]] = []

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: Model,
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.dependants.clear()
        if self.parent:
            self.parent_lookup_kwarg = f"{self.parent}__exact"
        super().__init__(field, request, params, model, model_admin, field_path)
        for _pos, entry in enumerate(model_admin.list_filter):
            if isinstance(entry, (list, tuple)) and (
                len(entry) == 2  # noqa: PLR2004
                and entry[0] != self.field_path
                and entry[1].__name__ == type(self).__name__
                and entry[1].parent == self.field_path
            ):
                kwarg = f"{entry[0]}__exact"
                if entry[1].parent and kwarg not in self.dependants:
                    self.dependants.extend(entry[1].dependants)
                    self.dependants.append(kwarg)

    def has_output(self) -> bool:
        if self.parent:
            return self.parent_lookup_kwarg in self.request.GET
        return True

    def choices(self, changelist: ChangeList) -> list[str]:
        to_remove = [self.lookup_kwarg, self.lookup_kwarg_isnull]
        p = changelist.params.copy()
        to_remove.extend(f for f in p if f in self.dependants)

        self.query_string = changelist.get_query_string(remove=to_remove)
        if self.lookup_val:
            return [str(self.target_model.objects.get(pk=self.lookup_val)) or ""]
        return []

    def get_url(self) -> str:
        url = reverse(f"{self.admin_site.name}:autocomplete")
        if self.parent_lookup_kwarg in self.request.GET:
            flt = self.parent_lookup_kwarg.split("__")[-2]
            oid = self.request.GET[self.parent_lookup_kwarg]
            return f"{url}?{flt}={oid}"
        return url

    @classmethod
    def factory(cls, *, title: str | None = None, lookup_name: str = "exact", **kwargs: Any) -> "type":
        kwargs["filter_title"] = title
        kwargs["lookup_name"] = lookup_name
        return type("LinkedAutoCompleteFilter", (cls,), kwargs)
