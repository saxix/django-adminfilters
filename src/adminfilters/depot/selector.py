from urllib.parse import urlencode

from django.contrib.admin import ListFilter

from adminfilters.depot.models import StoredFilter


def get_query_string(request, new_params=None, remove=None):
    if new_params is None:
        new_params = {}
    if remove is None:
        remove = []
    p = dict(request.GET.items()).copy()
    for r in remove:
        for k in list(p):
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    return '?%s' % urlencode(sorted(p.items()))


class FilterDepotManager(ListFilter):
    title = "Saved Filters"
    template = 'adminfilters/selector.html'
    parameter_newname = "adminfilters_filter_save"
    parameter_selection = "adminfilters_filter_select"
    parameter_shared = "adminfilters_filter_shared"

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.request = request
        self.model_admin = model_admin
        self.selected_filter = params.pop(self.parameter_selection, None)
        self.save_as = params.pop(self.parameter_newname, None)
        self.can_add_filter = request.user.has_perm('depot.add_storefilter')

    def has_output(self):
        return True

    def operation(self):
        if self.selected:
            return "update"
        return "add"

    def queryset(self, request, queryset):
        if self.save_as:
            qs = get_query_string(request, {}, [self.parameter_newname,
                                                self.parameter_selection])
            StoredFilter.objects.update_or_create(owner=request.user,
                                                  defaults={
                                                      'name': self.save_as,
                                                      'query_string': qs
                                                  })
            self.model_admin.message_user(self.request, f"Filter '{self.save_as}' successfully saved")
        return queryset

    def choices(self, changelist):
        self.query_string = get_query_string(self.request, {}, [self.parameter_newname,
                                                                self.parameter_selection])
        self.selected = False
        for f in StoredFilter.objects.all():
            self.selected = self.selected or str(self.query_string) == str(f.query_string)
            yield {
                'selected': str(self.query_string) == str(f.query_string),
                'query_string': f.query_string,
                'pk': f.pk,
                'name': f.name,
            }
