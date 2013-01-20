from django.contrib.admin import ModelAdmin
from ichangelist.changelist import IChangeList
from .models import DemoModel
from django.contrib.auth.admin import UserAdmin

class DemoModelAdmin(ModelAdmin):
#    list_display = ('char', 'integer', 'logic', 'null_logic',)
    list_display = [f.name for f in DemoModel._meta.fields]



class IUserAdmin(UserAdmin):
    cell_filter = ['email']

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        from django.contrib.admin.views.main import ChangeList
        return IChangeList
