# Autocomplete Filters

## AutoComplete

![autocomplete](../static/images/autocomplete.gif){width=200}


This filter is for ForeignKeys and uses select2_ javascript. It is based on the standard Django
[autocomplete](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields) implementation, no external libraries are needed.

See Django autocomplete_ documentation for the ajax service options.


### Usage


    class MyCountry(models.ModelAdmin):
        search_fields = ('name', )

    class MyModelAdmin(AdminFiltersMixin, models.ModelAdmin):
        list_filter = (
            ('country', AutoCompleteFilter),
            ...
            )




## LinkedAutoComplete

![autocomplete](../static/images/autocomplete.gif){width=200,align=center}



As filter_autocomplete_ it can be used in case dependant master/details elements where we want to limits the "details" based on the "master" selection.


### Usage

    class Country(models.Model):
        ...

    class Region(models.Model):
        country = models.ForeignKey(Country, ...)

    class MyModel(models.Model):
        region = models.ForeignKey(Region, ...)

    class MyCountry(AdminAutoCompleteSearchMixin, models.ModelAdmin):
        search_fields = ('name', )

    class MyRegion(AdminAutoCompleteSearchMixin, models.ModelAdmin):
        search_fields = ('name', )

    class MyModelAdmin(AdminFiltersMixin, models.ModelAdmin):
        list_filter = (
            ('region__country', LinkedAutoCompleteFilter.factory(parent=None)),
            ('region', LinkedAutoCompleteFilter.factory(parent="region__country")),
            ...
            )
