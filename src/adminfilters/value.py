import json

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from adminfilters.mixin import MediaDefinitionFilter, SmartFieldListFilter


class ValueFilter(MediaDefinitionFilter, SmartFieldListFilter):
    template = "adminfilters/value.html"
    toggleable = False
    filter_title = None
    lookup_name = "exact"
    button = True
    can_negate = True
    negated = False

    def __init__(self, field, request, params, model, model_admin, field_path):
        # self.lookup_negated_val = None
        # self.model = model
        # self.field = field
        # self.lookup_val = None
        # self.lookup_kwarg = '%s__%s' % (field_path, self.lookup_name)
        # self.lookup_kwarg_negated = '%s__negate' % self.lookup_kwarg
        # self.parse_query_string(params)
        self.lookup_kwarg = None
        self.lookup_kwarg_negated = None
        self.field_path = field_path
        self.parameters = {}
        self.filters = {}
        for p in self.expected_parameters():
            if p in params:
                self.parameters[p] = params.pop(p)

        super().__init__(field, request, params, model, model_admin, field_path)
        self._params = self.parameters
        self.title = self._get_title()
        # self.query_string = get_query_string(request, remove=self.expected_parameters())

        # self.params = params
        # self.query_values = []
        # self.operator = '+'

    def expected_parameters(self):
        self.lookup_kwarg = "%s__%s" % (self.field_path, self.lookup_name)
        self.lookup_kwarg_negated = "%s__negate" % self.lookup_kwarg
        return [self.lookup_kwarg, self.lookup_kwarg_negated]

    def value(self):
        return [
            self.get_parameters(self.lookup_kwarg),
            self.get_parameters(self.lookup_kwarg_negated) == "true",
            # self.parameters[self.lookup_kwarg],
            # self.parameters[self.lookup_kwarg_negated] == 'true'
            # self.lookup_val,
            # self.lookup_negated_val == 'true'
        ]

    def js_options(self):
        return json.dumps(
            dict(button=self.button, canNegate=self.can_negate, negated=self.negated)
        )

    def _get_title(self):
        if self.filter_title:
            return self.filter_title
        elif "__" in self.field_path:
            return self.field_path.replace("__", "->")
        return getattr(self.field, "verbose_name", self.field_path)

    @classmethod
    def factory(cls, *, title=None, lookup_name="exact", **kwargs):
        kwargs["filter_title"] = title
        kwargs["lookup_name"] = lookup_name
        return type("ValueFilter", (cls,), kwargs)

    # def parse_query_string(self, params):
    #     self.lookup_negated_val = params.get(self.lookup_kwarg_negated)
    #     self.lookup_val = params.get(self.lookup_kwarg, '')

    def queryset(self, request, queryset):
        target, exclude = self.value()
        if target:
            try:
                self.filters = {self.lookup_kwarg: target}
                if exclude:
                    queryset = queryset.exclude(**self.filters)
                else:
                    queryset = queryset.filter(**self.filters)
            except Exception as e:
                msg = _("%s filter ignored due to an error %s") % (self.title, e)
                self.model_admin.message_user(request, msg, messages.ERROR)
                pass
        return queryset

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(
            remove=self.expected_parameters()
        )
        return []

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
                "adminfilters/value%s.js" % extra,
            ),
            css={
                "screen": ("adminfilters/adminfilters.css",),
            },
        )


class MultiValueFilter(ValueFilter):
    template = "adminfilters/value_multi.html"
    separator = ","
    filter_title = None
    lookup_name = "in"

    def placeholder(self):
        return _("comma separated list of values")

    def value(self):
        values = self.get_parameters(self.lookup_kwarg, None, multi=True)
        return [values, self.get_parameters(self.lookup_kwarg_negated, "") == "true"]


TextFieldFilter = ValueFilter
ForeignKeyFieldFilter = TextFieldFilter
MultiValueTextFieldFilter = MultiValueFilter
