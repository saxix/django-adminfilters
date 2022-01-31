
def get_attr(obj, attr, default=None):
    """Recursive get object's attribute. May use dot notation.

    """
    if '.' not in attr:
        return getattr(obj, attr, default)
    else:
        L = attr.split('.')
        return get_attr(getattr(obj, L[0], default), '.'.join(L[1:]), default)
