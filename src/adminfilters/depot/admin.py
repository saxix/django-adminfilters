from django.contrib import admin
from django.contrib.admin import register

from ..combo import RelatedFieldComboFilter
from .models import StoredFilter


@register(StoredFilter)
class StoredFilterAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "owner", "content_type")
    raw_id_fields = ("owner", "content_type")
    list_filter = (("content_type", RelatedFieldComboFilter),)
