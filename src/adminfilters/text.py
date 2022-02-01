from django import forms
from django.conf import settings
from django.contrib.admin import FieldListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language

from adminfilters.mixin import MediaDefinitionFilter


class TextFieldFilter(MediaDefinitionFilter, FieldListFilter):
    template = 'adminfilters/text.html'
    separator = ","
    toggleable = False
    filter_title = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_negated_val = None
        self.lookup_val = None
        self.lookup_kwarg = field_path
        self.lookup_kwarg_negated = "%s__negate" % field_path
        self.parse_query_string(params)
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = self.get_title()
        self.params = params
        self.query_values = []
        self.operator = '+'

    def get_title(self):
        if self.filter_title:
            return self.filter_title
        elif '__' in self.field_path:
            return self.field_path.replace('__', '->')
        return getattr(self.field, 'verbose_name', self.field_path)

    @classmethod
    def factory(cls, **kwargs):
        kwargs['filter_title'] = kwargs.pop('title', None)
        return type('TextFieldFilter', (cls,), kwargs)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_negated]

    def value(self):
        return [
            self.lookup_val,
            self.lookup_negated_val == "true"
        ]

    def parse_query_string(self, params):
        self.lookup_negated_val = params.get(self.lookup_kwarg_negated)
        self.lookup_val = params.get(self.lookup_kwarg, "")

    def queryset(self, request, queryset):
        target, exclude = self.value()
        if target:
            filters = {self.lookup_kwarg: target}
            if exclude:
                return queryset.exclude(**filters)
            else:
                return queryset.filter(**filters)
        return queryset

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'adminfilters/text%s.js' % extra,
                                 ),
        )


class MultiValueTextFieldFilter(TextFieldFilter):
    template = 'adminfilters/text_multi.html'
    separator = ","
    filter_title = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        if not field_path.endswith('__in'):
            field_path = f"{field_path}__in"
        super().__init__(field, request, params, model, model_admin, field_path)

    def parse_query_string(self, params):
        raw_values = params.get(self.lookup_kwarg, "").split(self.separator)
        self.lookup_negated_val = params.get(self.lookup_kwarg_negated)
        self.lookup_val = [e.strip() for e in raw_values if e.strip()]


ForeignKeyFieldFilter = TextFieldFilter
