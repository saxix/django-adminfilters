from django.contrib.admin.filters import (AllValuesFieldListFilter,
                                          RelatedFieldListFilter,
                                          SimpleListFilter,)
from django.db.models.query_utils import Q
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _

try:
    from django.db.models.fields.related import ForeignObjectRel
except ImportError:
    from django.db.models.related import RelatedObject as ForeignObjectRel


class AllValuesComboFilter(AllValuesFieldListFilter):
    template = 'adminfilters/combobox.html'


class AllValuesRadioFilter(AllValuesFieldListFilter):
    template = 'adminfilters/fieldradio.html'


class RelatedFieldComboFilter(RelatedFieldListFilter):
    template = 'adminfilters/fieldcombobox.html'


class RelatedFieldRadioFilter(RelatedFieldListFilter):
    template = 'adminfilters/fieldradio.html'


class RelatedFieldCheckBoxFilter(RelatedFieldListFilter):
    template = 'adminfilters/fieldcheckbox.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.model_admin = model_admin
        super(RelatedFieldCheckBoxFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.lookup_val = request.GET.getlist(self.lookup_kwarg, [])

    def queryset(self, request, queryset):
        if not len(self.lookup_val):
            return queryset

        filters = []
        for val in self.lookup_val:
            filters.append(Q(**{self.lookup_kwarg: val}))

        query = filters.pop()
        for item in filters:
            query |= item

        return queryset.filter(query)

    def choices(self, cl):
        try:
            from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        except ImportError:
            EMPTY_CHANGELIST_VALUE = self.model_admin.get_empty_value_display()

        yield {
            'selected': not len(self.lookup_val) and not self.lookup_val_isnull,
            'query_string': cl.get_query_string(
                {},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        yield {
            'selected': self.lookup_val_isnull,
            'query_string': cl.get_query_string({self.lookup_kwarg_isnull: 1},
                                                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('None'),
        }
        for pk_val, val in self.lookup_choices:
            yield {
                'selected': smart_text(pk_val) in self.lookup_val,
                'query_string': cl.get_query_string(
                    {
                        self.lookup_kwarg: pk_val,
                    },
                    [self.lookup_kwarg_isnull]),
                'display': val,
            }
        if (isinstance(self.field, ForeignObjectRel) and
                self.field.field.null or
                hasattr(self.field, 'rel') and
                self.field.null):
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string(
                    {
                        self.lookup_kwarg_isnull: 'True',
                    },
                    [self.lookup_kwarg]),
                'display': EMPTY_CHANGELIST_VALUE,
            }


class StartWithFilter(SimpleListFilter):
    prefixes = None
    lookup_val = None

    def lookups(self, request, model_admin):
        return self.prefixes

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == '--':
            k = [prefix for prefix, label in self.prefixes]
            query = Q()
            for el in k:
                query |= Q(codename__startswith=el)
            return queryset.exclude(query)
        else:
            return queryset.filter(codename__startswith=self.value())


class PermissionPrefixFilter(StartWithFilter):
    title = 'Permission'
    parameter_name = 'perm'
    prefixes = (('add', 'Add'), ('change', 'Change'), ('delete', 'Delete'), ('--', 'Others'))
