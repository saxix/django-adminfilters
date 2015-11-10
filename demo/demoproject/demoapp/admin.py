from adminfilters.filters import RelatedFieldCheckBoxFilter, RelatedFieldRadioFilter
from adminfilters.multiselect import UnionFieldListFilter, IntersectionFieldListFilter
from django.contrib.admin import ModelAdmin
from .models import DemoModel, DemoRelated
from django.contrib.auth.admin import UserAdmin

class DemoModelAdmin_RelatedFieldCheckBoxFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldCheckBoxFilter),)

class DemoModelAdmin_RelatedFieldRadioFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldRadioFilter),)

class DemoModelAdmin_UnionFieldListFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', UnionFieldListFilter),)

class DemoModelAdmin_IntersectionFieldListFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', IntersectionFieldListFilter),)

class DemoRelatedModelAdmin(ModelAdmin):
    list_display = [f.name for f in DemoRelated._meta.fields]

class IUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff')
