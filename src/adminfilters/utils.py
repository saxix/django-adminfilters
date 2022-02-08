import re
from urllib.parse import urlencode

from django.core.exceptions import FieldError

rex = re.compile("'.*'")


def get_message_from_exception(e: FieldError):
    message = str(e)
    fieldname = rex.findall(message) or ['']
    if 'Unsupported lookup' in message:
        return f'Unsupported lookup: {fieldname[0]}'
    elif 'resolve keyword' in message:
        return f'Unknown field or lookup: {fieldname[0]}'
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
    return '?%s' % urlencode(sorted(p.items()))
