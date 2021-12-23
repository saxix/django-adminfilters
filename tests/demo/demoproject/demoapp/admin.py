from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from adminfilters.autocomplete import AutoCompleteFilter
from adminfilters.filters import (ForeignKeyFieldFilter,
                                  RelatedFieldCheckBoxFilter,
                                  RelatedFieldRadioFilter, TextFieldFilter,)
from adminfilters.multiselect import (IntersectionFieldListFilter,
                                      UnionFieldListFilter,)

from .models import DemoModel, DemoRelated


class DemoModelAdmin_RelatedFieldCheckBoxFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldCheckBoxFilter),
                   ForeignKeyFieldFilter.factory('demo_related__name__icontains'),
                   TextFieldFilter.factory('name'),
                   )
    search_fields = ('name',)


class DemoModelAdmin_RelatedFieldRadioFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldRadioFilter),)
    search_fields = ('name',)


class DemoModelAdmin_UnionFieldListFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', UnionFieldListFilter),)
    search_fields = ('name',)


class DemoModelAdmin_IntersectionFieldListFilter(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', IntersectionFieldListFilter),)
    search_fields = ('name',)


class DemoModelModelAdmin(ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (
        ForeignKeyFieldFilter.factory('demo_related__name__istartswith'),
        TextFieldFilter.factory('name'),
        ('demo_related', AutoCompleteFilter)
    )
    search_fields = ('name',)


class DemoRelatedModelAdmin(ModelAdmin):
    list_display = [f.name for f in DemoRelated._meta.fields]
    search_fields = ('name',)


class IUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff')
    list_filter = TextFieldFilter.factory('username__istartswith'),
