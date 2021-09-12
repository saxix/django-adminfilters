from functools import wraps

from django.urls import reverse
from django.utils.safestring import mark_safe

from adminfilters.filters import TextFieldFilter


def textfieldfilter(lookup, short_description=None):
    def decorator(f):
        @wraps(f)
        def _inner(modeladmin, obj):
            try:
                field_name = lookup.split('__')[0]
                query_arg = lookup.replace('__', '|')
                value = getattr(obj, field_name)
                base_url = reverse(f"admin:{modeladmin.opts.app_label}_{modeladmin.opts.model_name}_changelist")
                filter = f'{value} <a href="{base_url}?{query_arg}={value}"><small>filter</small></a>'
                return mark_safe(filter)
            except Exception as e:
                raise

        _inner.lookup = lookup
        _inner.short_description = short_description or lookup
        _inner.textfieldfilter = True
        return _inner

    return decorator


class CellFilterMixin:
    def get_list_display(self, request):
        values = super().get_list_display(request)
        for v in values:
            if hasattr(self, v) and hasattr(getattr(self, v), 'textfieldfilter'):
                handler = getattr(self, v)
                for f in self.list_filter:
                    if isclass(f) and issubclass(f, TextFieldFilter):
                        if f.parameter_name == handler.lookup.replace('__', '|'):
                            break
                else:
                    raise Exception(f"'Invalid textfieldfilter {handler.__name__}. "
                                    f"Add `TextFieldFilter.factory('{handler.lookup}')` to `{self.__class__.__name__}.list_filter` '")
        return values
    #
    # @textfieldfilter('card_type__istartswith', short_description='Cart type')
    # def _card_type(self, obj):
    #     pass
    #
    # @textfieldfilter('service_provider__istartswith', short_description='service provider')
    # def _service_provider(self, obj):
    #     pass
