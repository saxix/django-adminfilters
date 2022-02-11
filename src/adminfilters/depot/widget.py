from django import forms
from django.conf import settings
from django.contrib.admin import ListFilter
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language

from adminfilters.depot.models import StoredFilter
from adminfilters.utils import get_query_string

from ..mixin import WrappperMixin


class DepotManager(WrappperMixin, ListFilter):
    title = 'Saved Filters'
    template = 'adminfilters/widget.html'
    parameter_name = 'adminfilters_filter_save'

    def __init__(self, request, params, model, model_admin):
        self.model_admin = model_admin
        super().__init__(request, params, model, model_admin)
        self.request = request
        self.query_string = get_query_string(self.request, {}, self.expected_parameters())
        self.can_add_filter = request.user.has_perm('depot.add_storedfilter')
        self.content_type = ContentType.objects.get_for_model(model_admin.model)
        if self.parameter_name in params:
            self.used_parameters[self.parameter_name] = params.pop(self.parameter_name)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.parameter_name]

    def queryset(self, request, queryset):
        if self.used_parameters:
            filter_name = self.used_parameters[self.parameter_name]
            qs = get_query_string(request, {}, self.expected_parameters())

            StoredFilter.objects.update_or_create(content_type=self.content_type,
                                                  name=filter_name,
                                                  defaults={
                                                      'query_string': qs,
                                                      'owner': request.user,
                                                  })
            self.model_admin.message_user(self.request, f"Filter '{filter_name}' successfully saved")
        return queryset

    def choices(self, changelist):
        self.selected = False
        for f in StoredFilter.objects.filter(content_type=self.content_type).order_by('name'):
            self.selected = self.selected or str(self.query_string) == str(f.query_string)
            yield {
                'selected': str(self.query_string) == str(f.query_string),
                'query_string': f.query_string,
                'name': f.name,
            }

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'adminfilters/depot%s.js' % extra,
                                 ),
            css={
                'screen': (
                    'adminfilters/adminfilters.css',
                ),
            },
        )
