from django import forms
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language

from .mixin import MediaDefinitionFilter


class GenericLookupFieldFilter(MediaDefinitionFilter, SimpleListFilter):
    template = 'adminfilters/lookup.html'
    parameter_name = None
    path_separator = '>'
    arg_separator = '|'
    can_negate = True
    negated = False
    lookup_field = None

    def __init__(self, request, params, model, model_admin):
        self.lookup_val = None
        self.lookup_negated = None

        super().__init__(request, params, model, model_admin)
        self.parse_query_string()

    @classmethod
    def factory(cls, lookup, **kwargs):
        if '__' not in lookup:
            lookup = f'{lookup}__exact'

        kwargs['lookup_field'] = lookup
        kwargs['id'] = kwargs.pop('id', lookup)
        kwargs['path_separator'] = kwargs.pop('path_separator', cls.path_separator)
        kwargs['arg_separator'] = kwargs.pop('arg_separator', cls.arg_separator)
        kwargs['title'] = kwargs.pop('title', lookup.replace('__', '->'))
        kwargs['parameter_name'] = lookup.replace('__', cls.path_separator)

        return type('GenericLookupFieldFilter', (cls,), kwargs)

    def parse_query_string(self):
        raw = self.used_parameters.get(self.parameter_name, self.arg_separator)
        self.lookup_val, self.lookup_negated = raw.split(self.arg_separator)

    def has_output(self):
        return True

    def value(self):
        return [self.lookup_val,
                (self.can_negate and self.lookup_negated == "true") or self.negated
                ]

    def queryset(self, request, queryset):
        target, exclude = self.value()
        if target:
            filters = {self.lookup_field: target}
            if exclude:
                return queryset.exclude(**filters)
            else:
                return queryset.filter(**filters)
        return queryset

    def lookups(self, request, model_admin):
        return []

    def choices(self, changelist):
        self.query_string = changelist.get_query_string({}, [self.parameter_name])
        yield {}

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'adminfilters/lookup%s.js' % extra,
                                 ),
            css={
                'screen': (
                    'admin/css/vendor/select2/select2%s.css' % extra,
                    'adminfilters/adminfilters.css',
                ),
            },
        )
