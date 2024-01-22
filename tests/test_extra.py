from django.contrib.auth.models import Permission

from adminfilters.compat import DJANGO_MAJOR
from adminfilters.extra import PermissionPrefixFilter


def test_GenericLookupFieldFilter(db):
    f = PermissionPrefixFilter

    if DJANGO_MAJOR < 5:
        param = "add"
    else:
        param = ["add"]
    qs = f(None, {"perm": param}, None, None).queryset(None, Permission.objects.all())
    assert qs.first().codename.startswith("add_")

    if DJANGO_MAJOR < 5:
        param = "change"
    else:
        param = ["change"]
    qs = f(None, {"perm": param}, None, None).queryset(
        None, Permission.objects.all()
    )
    assert qs.first().codename.startswith("change_")

    if DJANGO_MAJOR < 5:
        param = "delete"
    else:
        param = ["delete"]
    qs = f(None, {"perm": param}, None, None).queryset(
        None, Permission.objects.all()
    )
    assert qs.first().codename.startswith("delete_")

    qs = f(None, {}, None, None).queryset(None, Permission.objects.all())
    assert qs.exists()

    if DJANGO_MAJOR < 5:
        param = "--"
    else:
        param = ["--"]
    qs = f(None, {"perm": param}, None, None).queryset(None, Permission.objects.all())
    assert not qs.exists()
