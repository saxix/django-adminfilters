from django.contrib import admin
from django.contrib.admin import register

from .models import StoredFilter


@register(StoredFilter)
class StoredFilterAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'owner', "content_type")
