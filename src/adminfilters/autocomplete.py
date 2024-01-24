from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.forms import Media
from django.urls import reverse
from django.utils.translation import get_language

from .mixin import MediaDefinitionFilter, SmartFieldListFilter


def get_real_field(model, path):
    parts = path.split("__")
    current = model
    for p in parts:
        f = current._meta.get_field(p)
        if f.related_model:
            current = f.related_model
    return f


class AutoCompleteFilter(SmartFieldListFilter, MediaDefinitionFilter):
    template = "adminfilters/autocomplete.html"
    filter_title = None
    parent = None
    parent_lookup_kwarg = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.dependants = []
        self.lookup_kwarg = "%s__exact" % field_path
        self.lookup_kwarg_isnull = "%s__isnull" % field_path
        self._params = params
        self.request = request
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_val = self.get_parameters(self.lookup_kwarg)
        self.admin_site = model_admin.admin_site
        self.query_string = ""
        self.target_field = get_real_field(model, field_path)
        self.target_model = self.target_field.related_model

        self.target_opts = self.target_field.model._meta

        # if not hasattr(field, "get_limit_choices_to"):
        #     raise Exception(
        #         f"Filter '{field_path}' of {model_admin} is not supported by AutoCompleteFilter."
        #         f" Check your {model_admin}.list_filter value"
        #     )

        self.url = self.get_url()

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def get_url(self):
        return reverse("%s:autocomplete" % self.admin_site.name)

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(
            remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]
        )
        if self.lookup_val:
            get_kwargs = {self.field.target_field.name: self.lookup_val}
            return [str(self.target_model.objects.get(**get_kwargs)) or ""]
        return []

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (
            ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,) if i18n_name else ()
        )
        return Media(
            js=(
                "admin/js/vendor/jquery/jquery%s.js" % extra,
                "admin/js/vendor/select2/select2.full%s.js" % extra,
            )
            + i18n_file
            + (
                "admin/js/jquery.init.js",
                "admin/js/autocomplete.js",
                "adminfilters/autocomplete%s.js" % extra,
            ),
            css={
                "screen": (
                    "admin/css/vendor/select2/select2%s.css" % extra,
                    "adminfilters/adminfilters.css",
                ),
            },
        )

    @classmethod
    def factory(cls, *, title=None, lookup_name="exact", **kwargs):
        kwargs["filter_title"] = title
        kwargs["lookup_name"] = lookup_name
        return type("ValueFilter", (cls,), kwargs)

    def get_title(self):
        if not self.can_negate and self.negated:
            if self.negated_title:
                return self.negated_title
            else:
                return f"not {self.title}"
        return self.filter_title or self.title


class LinkedAutoCompleteFilter(AutoCompleteFilter):
    parent = None
    parent_lookup_kwarg = None
    extras = []
    dependants = []

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.dependants = []
        if self.parent:
            self.parent_lookup_kwarg = f"{self.parent}__exact"
        super().__init__(field, request, params, model, model_admin, field_path)
        for pos, entry in enumerate(model_admin.list_filter):
            if (
                isinstance(entry, (list, tuple))
                and len(entry) == 2
                and entry[0] != self.field_path
                and entry[1].__name__ == type(self).__name__
                and entry[1].parent == self.field_path
            ):
                kwarg = f"{entry[0]}__exact"
                if entry[1].parent:
                    if kwarg not in self.dependants:
                        self.dependants.extend(entry[1].dependants)
                        self.dependants.append(kwarg)

    def has_output(self):
        if self.parent:
            return self.parent_lookup_kwarg in self.request.GET
        return True

    def choices(self, changelist):
        to_remove = [self.lookup_kwarg, self.lookup_kwarg_isnull]
        p = changelist.params.copy()
        for f in p:
            if f in self.dependants:
                to_remove.append(f)

        self.query_string = changelist.get_query_string(remove=to_remove)
        if self.lookup_val:
            return [str(self.target_model.objects.get(pk=self.lookup_val)) or ""]
        return []

    def get_url(self):
        url = reverse("%s:autocomplete" % self.admin_site.name)
        if self.parent_lookup_kwarg in self.request.GET:
            flt = self.parent_lookup_kwarg.split("__")[-2]
            oid = self.request.GET[self.parent_lookup_kwarg]
            return f"{url}?{flt}={oid}"
        return url

    @classmethod
    def factory(cls, *, title=None, lookup_name="exact", **kwargs):
        kwargs["filter_title"] = title
        kwargs["lookup_name"] = lookup_name
        return type("LinkedAutoCompleteFilter", (cls,), kwargs)
