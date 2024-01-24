from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from .mixin import MediaDefinitionFilter, SmartListFilter
from .utils import cast_value, get_field_type, get_message_from_exception


class DjangoLookupFilter(MediaDefinitionFilter, SmartListFilter):
    parameter_name = "dj"
    title = "Django Lookup"
    template = "adminfilters/dj.html"
    can_negate = True
    negated = False
    button = True
    field_placeholder = _("field lookup. Es. name__startswith")
    placeholder = _("field value")

    def __init__(self, request, params, model, model_admin):
        self.lookup_kwarg_key = "%s__key" % self.parameter_name
        self.lookup_kwarg_value = "%s__value" % self.parameter_name
        self.lookup_kwarg_negated = "%s__negate" % self.parameter_name
        self._params = params
        self.lookup_field_val = self.get_parameters(self.lookup_kwarg_key, pop=True)
        self.lookup_value_val = self.get_parameters(self.lookup_kwarg_value, pop=True)
        self.lookup_negated_val = self.get_parameters(self.lookup_kwarg_negated, "false", pop=True)
        self.error_message = None
        self.exception = None
        self.filters = None
        self.exclude = None
        self.model = model
        self.query_string = None
        super().__init__(request, params, model, model_admin)

    @classmethod
    def factory(cls, **kwargs):
        return type("DjangoLookupFilter", (cls,), kwargs)

    def expected_parameters(self):
        return [
            self.lookup_kwarg_key,
            self.lookup_kwarg_value,
            self.lookup_kwarg_negated,
        ]

    def has_output(self):
        return True

    def value(self):
        try:
            if self.lookup_field_val:
                field, lookup, field_type = get_field_type(
                    self.model, self.lookup_field_val
                )
                value = cast_value(self.lookup_value_val, field, lookup)
                return [
                    self.lookup_field_val,
                    value,
                    (self.can_negate and self.lookup_negated_val == "true")
                    or self.negated,
                ]
        except ValidationError as e:  # pragma: no cover
            self.exception = e
            self.error_message = str(e.message)

        return [None, None, None]

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(
            remove=self.expected_parameters()
        )
        return []

    def queryset(self, request, queryset):
        try:
            key, value, negated = self.value()
            if key:
                try:
                    self.filters = Q(**{f"{self.lookup_field_val}": value})

                    if negated:
                        self.filters = ~self.filters

                    queryset = queryset.filter(self.filters)
                except FieldError as e:
                    self.exception = e
                    self.error_message = get_message_from_exception(e)
        except ValidationError as e:  # pragma: no cover
            self.exception = e
            self.error_message = str(e.message)

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
                "adminfilters/dj%s.js" % extra,
            ),
            css={
                "screen": ("adminfilters/adminfilters.css",),
            },
        )
