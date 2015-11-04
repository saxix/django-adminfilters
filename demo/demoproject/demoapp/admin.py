from adminfilters.filters import RelatedFieldCheckBoxFilter
from django.contrib.admin import ModelAdmin
from .models import DemoModel, DemoRelated
from django.contrib.auth.admin import UserAdmin

class DemoModelAdmin(ModelAdmin):
#    list_display = ('char', 'integer', 'logic', 'null_logic',)
    list_display = [f.name for f in DemoModel._meta.fields]
    list_filter = (('demo_related', RelatedFieldCheckBoxFilter),)


class DemoRelatedModelAdmin(ModelAdmin):
#    list_display = ('char', 'integer', 'logic', 'null_logic',)
    list_display = [f.name for f in DemoRelated._meta.fields]

class IUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff')
