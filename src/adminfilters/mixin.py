from django import forms
from django.contrib.admin.options import ModelAdmin


class AdminFiltersMixin(ModelAdmin):

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        for flt in cl.filter_specs:
            if hasattr(flt, 'media'):
                self.admin_filters_media += flt.media
        return cl

    def __init__(self, model, admin_site):
        self.admin_filters_media = forms.Media()
        super().__init__(model, admin_site)

    @property
    def media(self):
        original = super().media
        if hasattr(self, 'admin_filters_media'):
            original += self.admin_filters_media
        return original
