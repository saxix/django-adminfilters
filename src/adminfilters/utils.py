import logging
import re
from urllib.parse import urlencode

from django.core.exceptions import FieldError, ValidationError
from django.db import models
from django.db.models import BooleanField, DateField, DateTimeField

logger = logging.getLogger(__name__)

rex = re.compile("'.*'")


def parse_bool(value):
    if str(value).lower() in ["true", "1", "yes", "t", "y"]:
        return True
    elif str(value).lower() in ["false", "0", "no", "f", "n"]:
        return False
    return value


def get_message_from_exception(e: FieldError):
    message = str(e)
    fieldname = rex.findall(message) or [""]
    if "Unsupported lookup" in message:
        return f"Unsupported lookup: {fieldname[0]}"
    else:
        return message


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
    return "?%s" % urlencode(sorted(p.items()))


def get_field_by_name(model, name):
    field = model._meta.get_field(name)
    direct = not field.auto_created or field.concrete
    return field, field.model, direct, field.many_to_many


def get_all_field_names(model):
    from itertools import chain

    if not model:
        raise ValueError("'model' must be a Model instance")
    return list(
        set(
            chain.from_iterable(
                (field.name, field.attname)
                if hasattr(field, "attname")
                else (field.name,)
                for field in model._meta.get_fields()
                if not (field.many_to_one and field.related_model is None)
            )
        )
    )


def get_field_by_path(model, field_path):
    """
    get a Model class or instance and a path to a attribute, returns the field object

    :param model: :class:`django.db.models.Model`
    :param field_path: string path to the field
    :return: :class:`django.db.models.Field`


    >>> from django.contrib.auth.models import Permission

    >>> p = Permission(name='perm')
    >>> get_field_by_path(Permission, 'content_type').name
    'content_type'
    >>> p = Permission(name='perm')
    >>> get_field_by_path(p, 'content_type.app_label').name
    'app_label'
    """
    parts = field_path.split(".")
    target = parts[0]
    if not model:
        raise ValueError("'model' must be a Model instance")

    if target in get_all_field_names(model):
        field_object, model, direct, m2m = get_field_by_name(model, target)
        if isinstance(field_object, models.ForeignKey):
            if parts[1:]:
                while True:
                    if field_object.related_model is None:
                        break
                    fk = get_field_by_path(
                        field_object.related_model, ".".join(parts[1:])
                    )
                    if fk is None:
                        break
                    field_object = fk
                return field_object
            else:
                return field_object
        else:
            return field_object
    return None


def get_field_type(model, field_path):
    lookup = "exact"
    try:
        parts = field_path.split("__")
        field = get_field_by_path(model, ".".join(parts))
        if not field:
            raise ValidationError(f"Unknown field '{field_path}'")
        if field.name != parts[-1]:
            lookup = parts[-1]
        field_type = field.get_internal_type()
    except Exception:
        raise
    return field, lookup, field_type


def cast_value(v, fld, lookup, force=None):
    if force:
        func = force
    elif isinstance(fld, (BooleanField,)) or lookup in ["isnull"]:
        func = parse_bool
    elif (
        isinstance(
            fld,
            (
                DateField,
                DateTimeField,
            ),
        )
        and lookup
    ):
        return v
    else:
        func = fld.to_python
    if lookup in ["in"]:
        return [func(e) for e in v.split(",")]
    return func(v)
