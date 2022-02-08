from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.core.exceptions import FieldError
from django.db.models import Q
from django.utils.translation import get_language

from .mixin import MediaDefinitionFilter, SmartListFilter
from .utils import get_message_from_exception


class DjangoLookupFilter(MediaDefinitionFilter, SmartListFilter):
    parameter_name = 'adam'
    title = 'Django Lookup'
    template = 'adminfilters/dj.html'
    can_negate = True
    negated = False
    options = True
    true_values = ['_TRUE_', '_T_']
    false_values = ['_FALSE_', '_F_']

    def __init__(self, request, params, model, model_admin):
        self.lookup_kwarg_key = '%s__key' % self.parameter_name
        self.lookup_kwarg_value = '%s__value' % self.parameter_name
        self.lookup_kwarg_negated = '%s__negate' % self.parameter_name
        self.lookup_field_val = params.pop(self.lookup_kwarg_key, '')
        self.lookup_value_val = params.pop(self.lookup_kwarg_value, '')
        self.lookup_negated_val = params.pop(self.lookup_kwarg_negated, 'false')
        self.error_message = None
        self.exception = None
        self.filters = None
        self.exclude = None

        self.query_string = None
        super().__init__(request, params, model, model_admin)

    @classmethod
    def factory(cls, **kwargs):
        return type('DjangoLookupFilter', (cls,), kwargs)

    def expected_parameters(self):
        return [self.lookup_kwarg_key,
                self.lookup_kwarg_value,
                self.lookup_kwarg_negated]

    def has_output(self):
        return True

    def check_bool(self, value):
        if value in self.true_values:
            return True
        elif value in self.false_values:
            return False
        return value

    def value(self):
        if '__' in self.lookup_field_val:
            parts = self.lookup_field_val.split('__')
            op = parts[-1]
        else:
            op = 'exact'
        if op == 'in':
            value = [self.check_bool(e) for e in self.lookup_value_val.split(',')]
        else:
            value = self.check_bool(self.lookup_value_val)

        return [
            self.lookup_field_val,
            value,
            (self.can_negate and self.lookup_negated_val == 'true') or self.negated,
        ]

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    def queryset(self, request, queryset):
        key, value, negated = self.value()
        if key:
            try:
                self.filters = Q(**{f'{self.lookup_field_val}': value})

                if negated:
                    self.filters = ~self.filters

                queryset = queryset.filter(self.filters)
            except FieldError as e:
                self.exception = e
                self.error_message = get_message_from_exception(e)

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
