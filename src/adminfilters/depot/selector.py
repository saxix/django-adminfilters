from django.contrib.admin import ListFilter
from django.contrib.contenttypes.models import ContentType

from adminfilters.depot.models import StoredFilter
from adminfilters.utils import get_query_string

from ..mixin import WrappperMixin


class FilterDepotManager(WrappperMixin, ListFilter):
    title = 'Saved Filters'
    template = 'adminfilters/selector.html'
    parameter_newname = 'adminfilters_filter_save'
    # parameter_selection = 'adminfilters_filter_select'
    parameter_shared = 'adminfilters_filter_shared'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.request = request
        self.model_admin = model_admin
        # self.selected_filter = params.pop(self.parameter_selection, None)
        self.save_as = params.pop(self.parameter_newname, None)
        self.can_add_filter = request.user.has_perm('depot.add_storefilter')
        self.content_type = ContentType.objects.get_for_model(model_admin.model)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.parameter_newname]

    def queryset(self, request, queryset):
        if self.save_as:
            qs = get_query_string(request, {}, self.expected_parameters())
            StoredFilter.objects.update_or_create(content_type=self.content_type,
                                                  name=self.save_as,
                                                  defaults={
                                                      'query_string': qs,
                                                      'owner': request.user,
                                                  })
            self.model_admin.message_user(self.request, f"Filter '{self.save_as}' successfully saved")
        return queryset

    def choices(self, changelist):
        self.query_string = get_query_string(self.request, {}, self.expected_parameters())
        self.selected = False
        for f in StoredFilter.objects.filter(content_type=self.content_type).order_by('name'):
            self.selected = self.selected or str(self.query_string) == str(f.query_string)
            yield {
                'selected': str(self.query_string) == str(f.query_string),
                'query_string': f.query_string,
                # 'pk': f.pk,
                'name': f.name,
            }
