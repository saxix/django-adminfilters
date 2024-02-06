.. include:: ../globals.rst

.. _filters_autocomplete:


Autocomplete
============

.. image:: ../images/autocomplete.gif
    :width: 200


This filter is for ForeignKeys and uses select2_ javascript. It is based on the standard Django
autocomplete_ implementation, no external libraries are needed.

See Django autocomplete_ documentation for the ajax service options.


Usage
-----

python::

    class MyCountry(models.ModelAdmin):
        search_fields = ('name', )

    class MyModelAdmin(AdminFiltersMixin, models.ModelAdmin):
        list_filter = (
            ('country', AutoCompleteFilter),
            ...
            )




.. _autocomplete: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields



LinkedAutoComplete
==================

.. image:: ../images/autocomplete.gif
    :width: 200


As filter_autocomplete_ it can be used in case dependant master/details elements where we want to limits the "details" based on the "master" selection.


Usage
-----

python::

    class Country(models.ModelAdmin):
        ...

    class Region(models.ModelAdmin):
        country = models.ForeignKey(Country, ...)

    class MyModel(models.ModelAdmin):
        region = models.ForeignKey(Region, ...)

    class MyCountry(models.ModelAdmin):
        search_fields = ('name', )

    class MyRegion(models.ModelAdmin):
        search_fields = ('name', )

    class MyModelAdmin(AdminFiltersMixin, models.ModelAdmin):
        list_filter = (
            ('region__country', LinkedAutoCompleteFilter.factory(None),
            ('region', LinkedAutoCompleteFilter.factory("region__country"),
            ...
            )
