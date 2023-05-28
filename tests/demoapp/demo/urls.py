import django.contrib.admin.sites
import django.views.static
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import re_path

from adminfilters.depot.admin import StoredFilterAdmin
from adminfilters.depot.models import StoredFilter

from . import admin, models


class PublicAdminSite(django.contrib.admin.sites.AdminSite):
    def has_permission(self, request):
        request.user = User.objects.get_or_create(username="sax")[0]
        return True


public_site = PublicAdminSite()
django.contrib.admin.autodiscover()
public_site.register(
    models.Artist_RelatedFieldCheckBoxFilter,
    admin.DemoModelAdmin_RelatedFieldCheckBoxFilter,
)
public_site.register(
    models.Artist_RelatedFieldRadioFilter, admin.DemoModelAdmin_RelatedFieldRadioFilter
)
public_site.register(
    models.Artist_UnionFieldListFilter, admin.DemoModelAdmin_UnionFieldListFilter
)
public_site.register(
    models.Artist_IntersectionFieldListFilter,
    admin.DemoModelAdmin_IntersectionFieldListFilter,
)
public_site.register(models.Country, admin.CountryModelAdmin)
public_site.register(models.Band, admin.BandModelAdmin)
public_site.register(models.Artist, admin.ArtistModelAdmin)
public_site.register(models.DemoModelField, admin.DemoModelFieldAdmin)
public_site.register(User, admin.IUserAdmin)
public_site.register(StoredFilter, StoredFilterAdmin)

urlpatterns = (
    re_path(
        r"^(?P<path>favicon.ico)$",
        django.views.static.serve,
        {"document_root": settings.STATIC_ROOT},
    ),
    re_path(
        r"^static/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.STATIC_ROOT},
    ),
    re_path(r"", public_site.urls),
)
