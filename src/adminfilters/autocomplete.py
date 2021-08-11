import django
from django import forms
from django.conf import settings
from django.contrib.admin import FieldListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.urls import reverse
from django.utils.translation import get_language


class AutoCompleteFilter(FieldListFilter):
    template = 'adminfilters/autocomplete.html'
    url_name = '%s:%s_%s_autocomplete'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__%s__exact' % (field_path, field.target_field.name)
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)
        self.admin_site = model_admin.admin_site
        self.query_string = ""
        self.model = self.field.related_model
        self.model_name = model._meta.model_name
        self.app_label = model._meta.app_label
        self.field_name = field.name

        self.url = self.get_url()

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def get_url(self):
        if django.VERSION[:2] >= (3, 2):
            return reverse("admin:autocomplete")
        return reverse(self.url_name % (self.admin_site.name,
                                        self.model._meta.app_label,
                                        self.model._meta.model_name))

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull])
        if self.lookup_val:
            return [str(self.model.objects.get(pk=self.lookup_val)) or ""]
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
