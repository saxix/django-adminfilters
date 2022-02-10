import logging
from urllib import parse

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.core.exceptions import FieldError, ValidationError
from django.utils.translation import get_language, gettext as _

from .mixin import MediaDefinitionFilter, SmartListFilter
from .utils import cast_value, get_field_type, get_message_from_exception

logger = logging.getLogger(__name__)


class QueryStringFilter(MediaDefinitionFilter, SmartListFilter):
    parameter_name = 'qs'
    title = 'QueryString'
    template = 'adminfilters/querystring.html'
    can_negate = True
    negated = False
    options = True
    separator = ','

    def __init__(self, request, params, model, model_admin):
        self.parameter_name_negated = '%s__negate' % self.parameter_name
        self.lookup_field_val = params.pop(self.parameter_name, '')
        self.lookup_negated_val = params.pop(self.parameter_name_negated, 'false')
        self.query_string = None
        self.error_message = None
        self.exception = None
        self.filters = None
        self.exclude = None
        self.model_admin = model_admin
        self.model = model
        self.validation_errors = {}
        super().__init__(request, params, model, model_admin)

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
            if field_name[0] == '!':
                field_name = field_name[1:]
                target = exclude
            field, lookup, field_type = get_field_type(self.model, field_name)
            value = cast_value(raw_value, field, multiple=lookup in ['in'])
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
            except ValidationError as e:  # pragma: no cover
                self.exception = e
                self.error_message = str(e.message)
            except Exception as e:  # pragma: no cover
                logger.exception(e)
                self.exception = e
                if settings.DEBUG:
                    self.error_message = f'{e.__class__.__name__}: {e}'
                else:
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
            css={
                'screen': (
                    'adminfilters/adminfilters.css',
                ),
            },
        )
