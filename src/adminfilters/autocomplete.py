import django
from django import forms
from django.conf import settings
from django.contrib.admin import FieldListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.db.models import ManyToOneRel
from django.urls import reverse
from django.utils.translation import get_language


def get_real_field(model, path):
    parts = path.split('__')
    current = model
    for p in parts:
        f = current._meta.get_field(p)
        if f.related_model:
            current = f.related_model
    return f


class AutoCompleteFilter(FieldListFilter):
    template = 'adminfilters/autocomplete.html'
    url_name = '%s:%s_%s_autocomplete'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__exact' % field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path

        self.lookup_val = params.get(self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)
        self.admin_site = model_admin.admin_site
        self.query_string = ""
        self.target_field = get_real_field(model, field_path)
        self.target_model = self.target_field.related_model
        self.target_opts = self.target_field.model._meta
        if not hasattr(field, 'get_limit_choices_to'):
            raise Exception(f"Filter '{field_path}' of {model_admin} is not supported by AutoCompleteFilter."
                            f" Check your {model_admin}.list_filter value")

        # self.model_name = self.model._meta.model_name
        # self.app_label = self.model._meta.app_label
        # self.field_name = f.name
        # self.related_model = self.related_field.related_model

        self.url = self.get_url()

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def get_url(self):
        if django.VERSION[:2] >= (3, 2):
            return reverse("admin:autocomplete")
        return reverse(self.url_name % (self.admin_site.name,
                                        self.target_opts.app_label,
                                        self.target_opts.model_name))

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull])
        if self.lookup_val:
            # dump = {'self.model': self.model,
            #         'self.lookup_val': self.lookup_val,
            #         'self.model_name': self.model_name,
            #         'self.field_name': self.field_name,
            #         'self.lookup_kwarg': self.lookup_kwarg,
            #         'self.query_string': self.query_string,
            #         'self.related_field': self.related_field,
            #         'self.related_model': self.related_field.related_model,
            #         }
            # return [str(self.model.objects.get(**{self.field_name:self.lookup_val})) or ""]
            return [str(self.target_model.objects.get(pk=self.lookup_val)) or ""]
        return []

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                'admin/js/vendor/select2/select2.full%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'admin/js/autocomplete.js',
                                 'adminfilters/adminfilters%s.js' % extra,
                                 ),
            css={
                'screen': (
                    'admin/css/vendor/select2/select2%s.css' % extra,
                    'adminfilters/adminfilters.css',
                ),
            },
        )
