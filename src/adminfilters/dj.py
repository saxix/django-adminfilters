from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.db.models import Q
from django.utils.translation import get_language

from .mixin import MediaDefinitionFilter, SmartListFilter


class DjangoLookupFilter(MediaDefinitionFilter, SmartListFilter):
    parameter_name = "adam"
    title = "Django Lookup"
    template = "adminfilters/dj.html"
    can_negate = True
    negated = False
    options = True

    def __init__(self, request, params, model, model_admin):
        self.lookup_kwarg_key = "%s__key" % self.parameter_name
        self.lookup_kwarg_value = "%s__value" % self.parameter_name
        self.lookup_kwarg_negated = "%s__negate" % self.parameter_name
        self.lookup_field_val = params.pop(self.lookup_kwarg_key, "")
        self.lookup_value_val = params.pop(self.lookup_kwarg_value, "")
        self.lookup_negated_val = params.pop(self.lookup_kwarg_negated, "false")

        self.query_string = None
        super().__init__(request, params, model, model_admin)

    @classmethod
    def factory(cls, **kwargs):
        return type('JsonFieldFilter', (cls,), kwargs)

    def expected_parameters(self):
        return [self.lookup_kwarg_key,
                self.lookup_kwarg_value,
                self.lookup_kwarg_negated]

    def has_output(self):
        return True

    def value(self):
        return [
            self.lookup_field_val,
            self.lookup_value_val,
            (self.can_negate and self.lookup_negated_val == "true") or self.negated,
        ]

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    def queryset(self, request, queryset):
        key, value, negated = self.value()
        if key:
            filters = Q(**{f"{self.lookup_field_val}": str(value)})

            if negated:
                filters = ~filters
            else:
                filters = filters

            queryset = queryset.filter(filters)

        return queryset

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'adminfilters/dj%s.js' % extra,
                                 ),
        )
