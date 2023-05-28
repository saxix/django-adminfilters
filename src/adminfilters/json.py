from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.db.models import Q
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

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_key = "%s__key" % field_path
        self.lookup_kwarg_value = "%s__value" % field_path
        self.lookup_kwarg_negated = "%s__negate" % field_path
        self.lookup_kwarg_options = "%s__options" % field_path
        self.lookup_kwarg_type = "%s__type" % field_path
        self.lookup_key_val = params.get(self.lookup_kwarg_key, "")
        self.lookup_value_val = params.get(self.lookup_kwarg_value, "")
        self.lookup_negated_val = params.get(self.lookup_kwarg_negated, "false")
        self.lookup_options_val = params.get(self.lookup_kwarg_options, "e")
        self.lookup_type_val = params.get(self.lookup_kwarg_type, "any")

        self.field = field
        self.query_string = None
        self.field_path = field_path
        self.title = getattr(field, "verbose_name", field_path)
        super().__init__(field, request, params, model, model_admin, field_path)

    @classmethod
    def factory(cls, **kwargs):
        return type("JsonFieldFilter", (cls,), kwargs)

    def expected_parameters(self):
        return [
            self.lookup_kwarg_key,
            self.lookup_kwarg_value,
            self.lookup_kwarg_negated,
            self.lookup_kwarg_options,
            self.lookup_kwarg_type,
        ]

    def value(self):
        return [
            self.lookup_key_val,
            self.lookup_value_val,
            self.lookup_options_val,
            (self.can_negate and self.lookup_negated_val == "true") or self.negated,
            self.lookup_type_val,
        ]

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(
            remove=self.expected_parameters()
        )
        return []

    def queryset(self, request, queryset):
        key, value, options, negated, type_ = self.value()
        if key:
            if type_ == "any" and value.isnumeric():
                filters = Q(**{f"{self.field_path}__{key}": value}) | Q(
                    **{f"{self.field_path}__{key}": int(value)}
                )
            elif type_ == "num" and value.isnumeric():
                filters = Q(**{f"{self.field_path}__{key}": float(value)})
            else:  # type_ == 'str':
                filters = Q(**{f"{self.field_path}__{key}": str(value)})

            if negated:
                if self.options and options == "e":
                    filters = ~filters
                else:
                    filters = (
                        Q(**{f"{self.field_path}__{key}__isnull": True}) | ~filters
                    )
            else:
                if options == "i":
                    filters = filters | Q(**{f"{self.field_path}__{key}__isnull": True})

            queryset = queryset.filter(filters)

        return queryset

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (
            ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,) if i18n_name else ()
        )
        return forms.Media(
            js=("admin/js/vendor/jquery/jquery%s.js" % extra,)
            + i18n_file
            + (
                "admin/js/jquery.init.js",
                "adminfilters/jsonfilter%s.js" % extra,
            ),
            css={
                "screen": ("adminfilters/adminfilters.css",),
            },
        )
