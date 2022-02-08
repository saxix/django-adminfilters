from urllib import parse

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.core.exceptions import FieldError
from django.utils.translation import get_language, gettext as _

from adminfilters.mixin import MediaDefinitionFilter, SmartListFilter
from adminfilters.utils import get_message_from_exception


class QueryStringFilter(MediaDefinitionFilter, SmartListFilter):
    parameter_name = 'qs'
    title = 'QueryString'
    template = 'adminfilters/querystring.html'
    can_negate = True
    negated = False
    options = True
    separator = ','
    true_values = ['_TRUE_', '_T_']
    false_values = ['_FALSE_', '_F_']

    def __init__(self, request, params, model, model_admin):
        self.parameter_name_negated = '%s__negate' % self.parameter_name
        self.lookup_field_val = params.pop(self.parameter_name, '')
        self.lookup_negated_val = params.pop(self.parameter_name_negated, 'false')
        self.query_string = None
        self.error_message = None
        self.exception = None
        self.filters = None
        self.exclude = None
        super().__init__(request, params, model, model_admin)

    def check_bool(self, value):
        if value in self.true_values:
            return True
        elif value in self.false_values:
            return False
        return value

    @classmethod
    def factory(cls, **kwargs):
        return type('DjangoLookupFilter', (cls,), kwargs)

    def expected_parameters(self):
        return [self.parameter_name,
                self.parameter_name_negated]

    def has_output(self):
        return True

    def value(self):
        return [
            self.lookup_field_val,
            (self.can_negate and self.lookup_negated_val == 'true') or self.negated,
        ]

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    def get_filters(self, value):
        query_params = dict(parse.parse_qsl('&'.join(value.splitlines())))
        exclude = {}
        filters = {}

        for field_name, raw_value in query_params.items():
            target = filters
            if '__' in field_name:
                parts = field_name.split('__')
                op = parts[-1]
            else:
                op = 'exact'
            if field_name[0] == '!':
                field_name = field_name[1:]
                target = exclude

            if op == 'in':
                value = [self.check_bool(e) for e in raw_value.split(',')]
            else:
                value = self.check_bool(raw_value)

            target[field_name] = value

        return filters, exclude

    def queryset(self, request, queryset):
        value, negated = self.value()
        if value:
            try:
                self.filters, self.exclude = self.get_filters(value)
                if not (self.filters or self.exclude):
                    self.error_message = _('Invalid django filter')
                else:
                    if negated:
                        queryset = queryset.filter(**self.exclude).exclude(**self.filters)
                    else:
                        queryset = queryset.filter(**self.filters).exclude(**self.exclude)
            except FieldError as e:
                self.exception = e
                self.error_message = get_message_from_exception(e)
            except Exception as e:  # pragma: no cover
                self.exception = e
                self.error_message = 'Invalid filter'
        return queryset

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'adminfilters/querystring%s.js' % extra,
                                 ),
        )
