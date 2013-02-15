from django.contrib.admin.filters import RelatedFieldListFilter, AllValuesFieldListFilter
from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode


class CellFilter(object):
    title = ""
    menu_labels = {'lt': _('Less than'),
                   'gt': _('Greater than'),
                   'lte': _('Less or equals than'),
                   'gte': _('Greater or equals than'),
                   'exact': _('Equals to'),
                   'not': _('Not equals to'),
                   'rem': _('Remove filter')}

    def __init__(self, field, request, params, model, model_admin, field_path, column=None):
        self.column = column or field_path or field.name
        self.col_operators = model_admin.cell_filter_operators.get(field.name, ('exact', 'not'))
        self.seed = field_path


    def __repr__(self):
        return "<%s for `%s` as %s>" % (self.__class__.__name__, self.column, id(self))

    def is_active(self, cl):
        active_filters = cl.params.keys()
        for x in self.expected_parameters():
            if x in active_filters:
                return True
        return False

    def has_output(self):
        return True

    def get_menu_item_for_op(self, op):
        return CellFilter.menu_labels.get(op), '%s__%s' % (self.seed, op)

    def expected_parameters(self):
        expected_parameters = []
        for op in self.col_operators:
            filter = '%s__%s' % (self.seed, op)
            expected_parameters.append(filter)
        return expected_parameters


class ChoicesCellFilter(CellFilter, AllValuesFieldListFilter):
    pass


class BooleanCellFilter(CellFilter, AllValuesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path, column=None):
        self.col_operators = model_admin.cell_filter_operators.get(field.name, ('exact', 'not'))
        super(BooleanCellFilter, self).__init__(field, request, params, model, model_admin, field_path, column)

    def get_menu_item_for_op(self, op):
        if op in ('exact', ''):
            return _('Yes'), self.seed
        else:
            return _('No'), '%s__not' % self.seed

    def expected_parameters(self):
        expected_parameters = []
        ops = [op for op in self.col_operators if op != 'exact']
        expected_parameters.append(self.seed)
        for op in ops:
            filter = '%s__%s' % (self.seed, op)
            expected_parameters.append(filter)
        return expected_parameters


class FieldCellFilter(CellFilter, AllValuesFieldListFilter):
    def get_menu_item_for_op(self, op):
        if op == 'exact':
            return CellFilter.menu_labels.get(op), self.seed
        return CellFilter.menu_labels.get(op), '%s__%s' % (self.seed, op)

    def expected_parameters(self):
        expected_parameters = []
        ops = [op for op in self.col_operators if op != 'exact']
        expected_parameters.append(self.seed)
        for op in ops:
            filter = '%s__%s' % (self.seed, op)
            expected_parameters.append(filter)
        return expected_parameters


class RelatedFieldCellFilter(RelatedFieldListFilter, CellFilter):
    def __init__(self, field, request, params, model, model_admin, field_path, column=None):
        super(RelatedFieldCellFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.column = column or field_path or field.name
        self.col_operators = model_admin.cell_filter_operators.get(field.name, ('exact', 'not'))
        self.seed = "__".join(self.lookup_kwarg.split('__')[:-1])


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
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE

        yield {
            'selected': not len(self.lookup_val) and not self.lookup_val_isnull,
            'query_string': cl.get_query_string({},
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
                'selected': smart_unicode(pk_val) in self.lookup_val,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: pk_val,
                    }, [self.lookup_kwarg_isnull]),
                'display': val,
                }
        if (isinstance(self.field, models.related.RelatedObject)
            and self.field.field.null or hasattr(self.field, 'rel')
        and self.field.null):
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                    }, [self.lookup_kwarg]),
                'display': EMPTY_CHANGELIST_VALUE,
                }
