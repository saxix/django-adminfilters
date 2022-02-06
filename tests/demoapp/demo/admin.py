from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin

from adminfilters.autocomplete import AutoCompleteFilter
from adminfilters.combo import ChoicesFieldComboFilter
from adminfilters.depot.selector import FilterDepotManager
from adminfilters.filters import (DjangoLookupFilter, GenericLookupFieldFilter,
                                  IntersectionFieldListFilter, JsonFieldFilter,
                                  NumberFilter, QueryStringFilter,
                                  RelatedFieldCheckBoxFilter,
                                  RelatedFieldRadioFilter, UnionFieldListFilter,
                                  ValueFilter, )
from adminfilters.mixin import AdminFiltersMixin

from .models import Artist, Band, Country


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
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (('demo_related', RelatedFieldCheckBoxFilter),
                   )
    search_fields = ('name',)


class DemoModelAdmin_RelatedFieldRadioFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (('demo_related', RelatedFieldRadioFilter),)
    search_fields = ('name',)


class DemoModelAdmin_UnionFieldListFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (('demo_related', UnionFieldListFilter),)
    search_fields = ('name',)


class DemoModelAdmin_IntersectionFieldListFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (('demo_related', IntersectionFieldListFilter),)
    search_fields = ('name',)


class DemoModelFieldAdmin(DebugMixin, ModelAdmin):
    list_display = ("char", "integer", "logic", "email", "choices")
    list_filter = (
        ("choices", ChoicesFieldComboFilter),
        ("integer", NumberFilter),
    )


class CountryModelAdmin(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Country._meta.fields]
    search_fields = ('name',)


class BandModelAdmin(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Band._meta.fields]
    search_fields = ('name',)
    list_filter = ('genre',
                   )


class ArtistModelAdmin(DebugMixin, AdminFiltersMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (
        FilterDepotManager,
        QueryStringFilter,
        DjangoLookupFilter,
        GenericLookupFieldFilter.factory('name__istartswith', can_negate=False, negated=True),
        GenericLookupFieldFilter.factory('country__name__istartswith'),
        ("name", ValueFilter),
        ("last_name", ValueFilter.factory(title="LastName")),
        ("flags", JsonFieldFilter.factory(can_negate=False, options=False)),
        ('country', AutoCompleteFilter),
        ('year_of_birth', NumberFilter),
    )
    search_fields = ('name',)


class IUserAdmin(DebugMixin, UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff')
    list_filter = GenericLookupFieldFilter.factory('username__istartswith'),
