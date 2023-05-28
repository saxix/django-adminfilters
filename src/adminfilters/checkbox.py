from django.contrib.admin.filters import RelatedFieldListFilter
from django.db.models.fields.related import ForeignObjectRel
from django.db.models.query_utils import Q
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _

from .mixin import MediaDefinitionFilter, WrappperMixin
from .utils import parse_bool


class RelatedFieldCheckBoxFilter(
    WrappperMixin, MediaDefinitionFilter, RelatedFieldListFilter
):
    template = "adminfilters/checkbox.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.model_admin = model_admin
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg = "%s__%s" % (field_path, field.target_field.name)
        self.lookup_val = request.GET.getlist(self.lookup_kwarg, [])

    def queryset(self, request, queryset):
        filters = Q()
        if self.lookup_val:
            filters.add(Q(**{f"{self.lookup_kwarg}__in": self.lookup_val}), Q.OR)

        if self.lookup_val_isnull:
            filters.add(
                Q(**{self.lookup_kwarg_isnull: parse_bool(self.lookup_val_isnull)}),
                Q.OR,
            )
        return queryset.filter(filters)

    def choices(self, cl):
        try:
            from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        except ImportError:
            EMPTY_CHANGELIST_VALUE = self.model_admin.get_empty_value_display()

        uncheck_all = []
        uncheck_all.append("{}={}".format(self.lookup_kwarg_isnull, 1))
        for i in self.lookup_choices:
            uncheck_all.append("{}={}".format(self.lookup_kwarg, i[0]))

        yield {
            "selected": not len(self.lookup_val) and not self.lookup_val_isnull,
            "query_string": cl.get_query_string(
                {}, [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            "display": _("All"),
            "check_to_remove": "&".join(uncheck_all),
        }
        yield {
            "selected": self.lookup_val_isnull,
            "query_string": cl.get_query_string(
                {self.lookup_kwarg_isnull: 1},
                [self.lookup_kwarg, self.lookup_kwarg_isnull],
            ),
            "display": _("None"),
            "uncheck_to_remove": "{}=1".format(self.lookup_kwarg_isnull),
        }
        for pk_val, val in self.lookup_choices:
            yield {
                "selected": smart_str(pk_val) in self.lookup_val,
                "query_string": cl.get_query_string(
                    {
                        self.lookup_kwarg: pk_val,
                    },
                    [self.lookup_kwarg_isnull],
                ),
                "display": val,
                "uncheck_to_remove": "{}={}".format(self.lookup_kwarg, pk_val)
                if pk_val
                else "",
            }
        if (
            isinstance(self.field, ForeignObjectRel)
            and self.field.field.null
            or hasattr(self.field, "rel")
            and self.field.null
        ):
            yield {
                "selected": bool(self.lookup_val_isnull),
                "query_string": cl.get_query_string(
                    {
                        self.lookup_kwarg_isnull: "True",
                    },
                    [self.lookup_kwarg],
                ),
                "uncheck_to_remove": "{}=1".format(self.lookup_kwarg_isnull),
                "display": EMPTY_CHANGELIST_VALUE,
            }
