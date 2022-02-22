from django.contrib.auth.models import Permission

from adminfilters.extra import PermissionPrefixFilter


def test_GenericLookupFieldFilter(db):
    f = PermissionPrefixFilter

    qs = f(None, {'perm': 'add'}, None, None).queryset(None, Permission.objects.all())
    assert qs.first().codename.startswith('add_')

    qs = f(None, {'perm': 'change'}, None, None).queryset(None, Permission.objects.all())
    assert qs.first().codename.startswith('change_')

    qs = f(None, {'perm': 'delete'}, None, None).queryset(None, Permission.objects.all())
    assert qs.first().codename.startswith('delete_')

    qs = f(None, {}, None, None).queryset(None, Permission.objects.all())
    assert qs.exists()

    qs = f(None, {'perm': '--'}, None, None).queryset(None, Permission.objects.all())
    assert not qs.exists()
