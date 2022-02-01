import django.contrib.admin.sites
from django.contrib.auth.models import User
from django.urls import re_path

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
public_site.register(models.DemoModel, admin.DemoModelModelAdmin)
public_site.register(models.DemoModelField, admin.DemoModelFieldAdmin)
public_site.register(User, admin.IUserAdmin)

urlpatterns = (
    re_path(r'', public_site.urls),
)
