from urllib.parse import urlencode


def parse_bool(value):
    if str(value).lower() in ['true', '1', 'yes', 't', 'y']:
        return True
    elif str(value).lower() in ['false', '0', 'no', 'f', 'n']:
        return False
    else:
        raise ValueError(value)


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
