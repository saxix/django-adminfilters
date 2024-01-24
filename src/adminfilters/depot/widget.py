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
    title = "Saved Filters"
    template = "adminfilters/widget.html"
    parameter_name = "adminfilters_depot"
    parameter_name_op = "adminfilters_depot_op"

    def __init__(self, request, params, model, model_admin):
        self.model_admin = model_admin
        self._params = params.copy()
        super().__init__(request, params, model, model_admin)
        self.request = request
        self.query_string = get_query_string(
            self.request, {}, self.expected_parameters()
        )
        self.can_add_filter = request.user.has_perm("depot.add_storedfilter")
        self.content_type = ContentType.objects.get_for_model(model_admin.model)
        for p in self.expected_parameters():
            if p in params:
                self.used_parameters[p] = params.pop(p)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.parameter_name, self.parameter_name_op]

    def queryset(self, request, queryset):
        filter_name = self.get_parameters(self.parameter_name)
        operation = self.get_parameters(self.parameter_name_op, "add")
        if filter_name:
            if operation == "add":
                qs = get_query_string(request, {}, self.expected_parameters())

                StoredFilter.objects.update_or_create(
                    content_type=self.content_type,
                    name=filter_name,
                    defaults={
                        "query_string": qs,
                        "owner": request.user,
                    },
                )
                self.model_admin.message_user(
                    self.request, f"Filter '{filter_name}' successfully saved"
                )
            elif operation == "delete":
                StoredFilter.objects.filter(id=filter_name).delete()
        return queryset

    def choices(self, changelist):
        self.selected = False
        for f in StoredFilter.objects.filter(content_type=self.content_type).order_by(
            "name"
        ):
            if str(self.query_string) == str(f.query_string):
                self.selected = True
                self.selected_id = f.pk

            yield {
                "selected": str(self.query_string) == str(f.query_string),
                "query_string": f.query_string,
                "name": f.name,
            }

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
                "adminfilters/depot%s.js" % extra,
            ),
            css={
                "screen": ("adminfilters/adminfilters.css",),
            },
        )
