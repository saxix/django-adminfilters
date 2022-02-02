from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin

from adminfilters.autocomplete import AutoCompleteFilter
from adminfilters.filters import (RelatedFieldCheckBoxFilter,
                                  RelatedFieldRadioFilter, TextFieldFilter,)
from adminfilters.json import JsonFieldFilter
from adminfilters.lookup import GenericLookupFieldFilter
from adminfilters.mixin import AdminFiltersMixin
from adminfilters.multiselect import (IntersectionFieldListFilter,
                                      UnionFieldListFilter,)
from adminfilters.numbers import NumberFilter

from .models import DemoModel, DemoRelated


class DebugChangeList(ChangeList):
    def get_queryset(self, request):
        try:
            return super().get_queryset(request)
        except IncorrectLookupParameters as e:
            raise Exception(str(e))

    def get_filters(self, request):
        try:
            return super().get_filters(request)
        except Exception as e:
            raise Exception(str(e))


class DebugMixin:
    def get_changelist(self, request, **kwargs):
        return DebugChangeList


class DemoModelAdmin_RelatedFieldCheckBoxFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldCheckBoxFilter),
                   )
    search_fields = ('name',)


class DemoModelAdmin_RelatedFieldRadioFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldRadioFilter),)
    search_fields = ('name',)


class DemoModelAdmin_UnionFieldListFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', UnionFieldListFilter),)
    search_fields = ('name',)


class DemoModelAdmin_IntersectionFieldListFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', IntersectionFieldListFilter),)
    search_fields = ('name',)


class DemoModelModelAdmin(DebugMixin, AdminFiltersMixin, ModelAdmin):
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (
        GenericLookupFieldFilter.factory('name__istartswith', can_negate=False, negated=True),
        GenericLookupFieldFilter.factory('demo_related__name__istartswith'),
        ("name", TextFieldFilter),
        ("last_name", TextFieldFilter.factory(title="LastName")),
        ("flags", JsonFieldFilter.factory(can_negate=False, options=False)),
        ('demo_related', AutoCompleteFilter)
    )
    search_fields = ('name',)


class DemoModelFieldAdmin(DebugMixin, ModelAdmin):
    list_filter = (
        ("integer", NumberFilter),
    )


class DemoRelatedModelAdmin(DebugMixin, ModelAdmin):
    list_display = [f.name for f in DemoRelated._meta.fields]
    search_fields = ('name',)


class IUserAdmin(DebugMixin, UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff')
    list_filter = GenericLookupFieldFilter.factory('username__istartswith'),
