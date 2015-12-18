import django.contrib.admin
import django.contrib.admin.sites
from django.conf.urls import include, url
from django.contrib.auth.models import User

from .demoapp import admin, models


class PublicAdminSite(django.contrib.admin.sites.AdminSite):

    def has_permission(self, request):
        request.user = User.objects.get_or_create(username='sax')[0]
        return True

public_site = PublicAdminSite()
django.contrib.admin.autodiscover()
public_site.register(models.DemoModel_RelatedFieldCheckBoxFilter,
                     admin.DemoModelAdmin_RelatedFieldCheckBoxFilter)
public_site.register(models.DemoModel_RelatedFieldRadioFilter,
                     admin.DemoModelAdmin_RelatedFieldRadioFilter)
public_site.register(models.DemoModel_UnionFieldListFilter,
                     admin.DemoModelAdmin_UnionFieldListFilter)
public_site.register(models.DemoModel_IntersectionFieldListFilter,
                     admin.DemoModelAdmin_IntersectionFieldListFilter)
public_site.register(models.DemoRelated, admin.DemoRelatedModelAdmin)
public_site.register(User, admin.IUserAdmin)

urlpatterns = (
    url(r'', include(include(public_site.urls))),
    url(r'^admin/', include(include(public_site.urls))),
)
