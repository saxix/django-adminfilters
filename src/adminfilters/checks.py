from django.contrib.admin import ListFilter
from django.core.checks import Error, register

from adminfilters.mixin import AdminFiltersMixin, MediaDefinitionFilter


@register()
def check_adminfilters_media(*args, **kwargs):
    errors = []
    try:
        from django.contrib.admin import site
        for model, model_admin in site._registry.items():
            if not isinstance(model_admin, AdminFiltersMixin):
                for filter_fields in model_admin.list_filter:
                    filter_class = None
                    if isinstance(filter_fields, tuple):
                        filter_class = filter_fields[1]
                    elif isinstance(filter_fields, ListFilter):
                        filter_class = filter_fields
                    if filter_class and issubclass(filter_class, MediaDefinitionFilter):
                        errors.append(Error(f'{model_admin} must inherit from AdminFiltersMixin'))
                        break
    except Exception:  # pragma: no-cover
        raise
    return errors
