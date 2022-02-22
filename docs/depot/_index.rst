.. include:: globals.rst
.. _depot:

=====
Depot
=====

.. versionadded:: 2.0

.. image:: ../images/depot.gif
    :width: 800


This optional django app allows you to store/retrieve filters configuration.
It is fully compatible with any filter


Install
-------

Just as any other Django application

.. code-block:: python
    :caption: settings.py

    # settings.py
    INSTALLED_APPS = (
        ...
        'django.contrib.admin',
        'adminfilters.depot',
        )


.. code-block:: python
    :caption: admin.py

    # admin.py
    from adminfilters.depot.widget import DepotManager
    from adminfilters.mixin import AdminFiltersMixin

    class ArtistModelAdmin(AdminFiltersMixin, ModelAdmin):
        list_filter = (
            DepotManager,
            ...
            )

Now you are able to store/retrieve filtering criteria for ``ArtistModelAdmin``.
Filters are stored in :class:StoredFilter model and availble thru ``StoredFilterAdmin``



.. _depot_widget:


DepotManager
------------

.. image:: ../images/depot.png
    :width: 200
