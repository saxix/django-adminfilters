from inspect import isclass
from typing import Any

from django.contrib.admin import ListFilter
from django.core.checks import Error, register

from adminfilters.mixin import AdminFiltersMixin, MediaDefinitionFilter


@register()
def check_adminfilters_media(*args: Any, **kwargs: Any) -> list[Error]:  # noqa: ARG001
    errors = []
    from django.contrib.admin import site  # noqa: PLC0415

    for model_admin in site._registry.values():
        if isclass(model_admin) and not issubclass(model_admin, AdminFiltersMixin):
            for filter_fields in model_admin.list_filter:
                filter_class = None
                if isinstance(filter_fields, tuple):
                    filter_class = filter_fields[1]
                elif isclass(filter_fields) and issubclass(filter_fields, (ListFilter,)):
                    filter_class = filter_fields

                if filter_class and issubclass(filter_class, MediaDefinitionFilter):
                    errors.append(
                        Error(
                            f"To use '{filter_class.__name__}', "
                            f"'{model_admin.__name__}' must inherit from 'AdminFiltersMixin'"
                        )
                    )
                    break

    return errors
