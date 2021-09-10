===================
django-adminfilters
===================

Collection of extra filters for the Django admin site

Demo can be found at https://django-smart-admin.herokuapp.com/


.. image:: https://travis-ci.org/saxix/django-adminfilters.svg?branch=develop
    :target: https://travis-ci.org/saxix/django-adminfilters

.. image:: https://codecov.io/github/saxix/django-adminfilters/coverage.svg?branch=develop
    :target: https://codecov.io/github/saxix/django-adminfilters?branch=develop

.. image:: https://badges.gitter.im/saxix/django-adminfilters.svg
    :target: https://gitter.im/saxix/django-adminfilters?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge


Filters
=======

* AutocompleteFilter
* AllValuesComboFilter
* AllValuesRadioFilter
* BooleanRadioFilter
* NumberFilter
* RelatedFieldComboFilter
* RelatedFieldRadioFilter
* RelatedFieldCheckBoxFilter
* StartWithFilter
* PermissionPrefixFilter
* MultipleSelectFieldListFilter
* IntersectionFieldListFilter
* UnionFieldListFilter
* ForeignKeyFieldFilter


Usage examples
==============

.. code-block:: python

    class UserAdmin(ModelAdmin):
        list_filter = (TextFieldFilter.factory('name__istartswith'),)



Run demo app
============

Note: django-adminfilters is also included in django-smart-admin, there is a running demo at https://django-smart-admin.herokuapp.com/



.. code-block:: bash

    $ git clone https://github.com/saxix/django-adminfilters.git
    $ cd django-adminfilters
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ make develop
    $ make demo


Project links
-------------

* Project home page: https://github.com/saxix/django-adminfilters
* Download: http://pypi.python.org/pypi/django-adminfilters/
