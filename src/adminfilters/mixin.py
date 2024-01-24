from django import forms
from django.contrib.admin import FieldListFilter, ListFilter
from django.contrib.admin.options import ModelAdmin
from django.core import checks

from adminfilters.compat import DJANGO_MAJOR


class WrappperMixin:
    negated = False
    can_negate = False
    title = None
    negated_title = None
    placeholder = ""

    def __init__(self, *args, **kwargs) -> None:
        self.error = None
        self.error_message = None
        super().__init__(*args, **kwargs)
        if (
            hasattr(self, "media")
            and self.model_admin
            and not isinstance(self.model_admin, AdminFiltersMixin)
        ):
            raise Exception(
                f"{self.model_admin.__class__.__name__} must inherit from AdminFiltersMixin"
            )

    def get_parameters(self, param_name, default="", multi=False, pop=False, separator=","):
        if pop:
            val = self._params.pop(param_name, default)
        else:
            val = self._params.get(param_name, default)
        if val:
            if DJANGO_MAJOR >= 5:
                if isinstance(val, list) and not multi:
                    val = val[-1]
            elif multi:
                val = val.split(separator)
        return val

    def html_attrs(self):
        classes = f"adminfilters box {self.__class__.__name__.lower()}"
        if self.error_message:
            classes += " error"

        return {
            "class": classes,
            "id": "_".join(self.expected_parameters()),
        }

    def get_title(self):
        if not self.can_negate and self.negated:
            if self.negated_title:
                return self.negated_title
            else:
                return f"not {self.title}"
        return self.title


class SmartListFilter(WrappperMixin, ListFilter):
    def __init__(self, request, params, model, model_admin):
        self.model_admin = model_admin
        self._params = params
        super().__init__(request, params, model, model_admin)


class SmartFieldListFilter(WrappperMixin, FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.model_admin = model_admin
        self._params = params
        super().__init__(field, request, params, model, model_admin, field_path)


class MediaDefinitionFilter:
    pass


class AdminFiltersMixin(ModelAdmin):
    def _check_linked_fields_modeladmin(self):
        from .autocomplete import LinkedAutoCompleteFilter

        linked_filters = [
            e
            for e in self.list_filter
            if isinstance(e, (list, tuple))
            and issubclass(e[1], LinkedAutoCompleteFilter)
        ]
        errs = []
        seen = []
        for pos, entry in enumerate(linked_filters):
            if entry[1] and entry[1].parent:
                parts = entry[1].parent.split("__")
                m = self.model
                for part in parts:
                    m = m._meta.get_field(part).remote_field.model
                    ma: ModelAdmin = self.admin_site._registry[m]
                    if ma not in seen and not isinstance(
                        ma, AdminAutoCompleteSearchMixin
                    ):
                        errs.append(
                            checks.Error(
                                f"{ma}` must inherits from AdminAutoCompleteSearchMixin",
                                obj=ma.__class__,
                                id="admin.E041",
                            )
                        )
                        seen.append(ma)

        return errs

    def _check_linked_fields_order(self):
        from .autocomplete import LinkedAutoCompleteFilter

        linked_filters = [
            e
            for e in self.list_filter
            if isinstance(e, (list, tuple))
            and issubclass(e[1], LinkedAutoCompleteFilter)
        ]
        errs = []
        seen = []
        for pos, entry in enumerate(linked_filters):
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

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_linked_fields_order(),
            *self._check_linked_fields_modeladmin(),
        ]

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        for flt in cl.filter_specs:
            if hasattr(flt, "media"):
                self.admin_filters_media += flt.media
        return cl

    def __init__(self, model, admin_site):
        self.admin_filters_media = forms.Media()
        super().__init__(model, admin_site)

    @property
    def media(self):
        original = super().media
        if hasattr(self, "admin_filters_media"):
            original += self.admin_filters_media
        return original


class AdminAutoCompleteSearchMixin(ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        field_names = [f.name for f in self.model._meta.get_fields()]
        filters = {k: v for k, v in request.GET.items() if k in field_names}
        queryset = queryset.filter(**filters)
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        return queryset, may_have_duplicates
