.. include:: ../globals.rst

.. _filters_value


MultiValueFilter
================

.. image:: ../images/multivalue.png
    :width: 200


Targets can be typed as comma separated list of values.

Usage
-----
::

    class MyModelAdmin(models.ModelAdmin):
        list_filter = (
            ('country__name', MultiValueFilter),
            ...
            )
:

Options
~~~~~~~

.. attribute:: JsonFilter.can_negate

    Control ability to work as `exclude` filter. Set to `False` hides the Exclude checkbox

.. attribute:: JsonFilter.placeholder

    Placeholder value for the Key input text. (Default. "JSON key")

.. attribute:: JsonFilter.template

    Template name used to render the filter. (Default. "adminfilters/value.html")

.. attribute:: JsonFilter.title

    Filter title. (Default. "<Field verbose_name>")

Configuration
~~~~~~~~~~~~~

The filter can be configured either using subclassing or `.factory()` method::

    class MyModelAdmin(models.ModelAdmin):
        list_filter = (
            ('name', MultiValueFilter.factory(can_negate=False, options=True,
                                              title=_("Person full name"))),
            ...
            )
