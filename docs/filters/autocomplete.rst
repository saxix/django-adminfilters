.. include:: ../globals.rst

.. _filters_autocomplete:


Autocomplete
============

.. image:: ../images/autocomplete.gif
    :width: 200


This filter is for ForeignKeys and uses select2_ javascript. It is based on the standard Django
autocomplete_ implementation, so no external libraries are needed.

See Django autocomplete_ documentation for the ajax service options.


Usage
-----

python::

    class MyCountry(models.ModelAdmin):
        search_fields = ('name', )

    class MyModelAdmin(models.ModelAdmin):
        list_filter = (
            ('country', AutoCompleteFilter),
            ...
            )




.. _autocomplete: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
