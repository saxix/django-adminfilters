from unittest.mock import MagicMock, Mock

from demo.models import Artist
from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from adminfilters.depot.models import StoredFilter
from adminfilters.depot.selector import FilterDepotManager


def test_save(admin_user, rf):
    request = rf.get('/')
    request.user = admin_user
    for m in [SessionMiddleware, MessageMiddleware]:
        m(MagicMock()).process_request(request)

    f = FilterDepotManager(request, {'adminfilters_filter_save': 'Filter1'}, None, ModelAdmin(Artist, Mock()))
    f.queryset(request, None)
    assert StoredFilter.objects.filter(name='Filter1').exists()


def test_choices(admin_user, rf):
    request = rf.get('/?a=1')
    request.user = admin_user
    for m in [SessionMiddleware, MessageMiddleware]:
        m(MagicMock()).process_request(request)
    StoredFilter.objects.create(name='Filter1',
                                content_type=ContentType.objects.get_for_model(Artist),
                                owner=admin_user,
                                query_string='?a=1')
    StoredFilter.objects.create(name='Filter2',
                                content_type=ContentType.objects.get_for_model(Artist),
                                owner=admin_user,
                                query_string='?a=2')

    f = FilterDepotManager(request, {'a': '1'}, None, ModelAdmin(Artist, Mock()))
    choices = list(f.choices(Mock()))
    assert len(choices) == 2
    assert choices[0] == {'name': 'Filter1', 'query_string': '?a=1', 'selected': True}
    assert choices[1] == {'name': 'Filter2', 'query_string': '?a=2', 'selected': False}
