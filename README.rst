===================
django-adminfilters
===================

Collection of extra filters for the Django admin site

Demo can be found at https://django-smart-admin.herokuapp.com/

.. image:: https://badge.fury.io/py/django-adminfilters.svg
    :target: https://badge.fury.io/py/django-adminfilters

.. image:: https://codecov.io/github/saxix/django-adminfilters/coverage.svg?branch=develop
    :target: https://codecov.io/github/saxix/django-adminfilters?branch=develop

.. image:: https://github.com/saxix/django-adminfilters/actions/workflows/test.yml/badge.svg
    :target: https://github.com/saxix/django-adminfilters/actions/workflows/test.yml


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

    class MyModel(models.Model):
        index = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
        age = models.IntegerField()
        flag = models.CharField(default="1", choices=(("0", "Flag 1"), ("1", "Flag 2"))
        household = models.ForeignKey('Household')
        custom = JSONField(default=dict, blank=True)

    class MyModelAdmin(ModelAdmin):
        list_filter = (
            ("custom", JsonFieldFilter.factory(can_negate=False, options=True)),
            ("flag", ChoicesFieldComboFilter),
            ('household', AutoCompleteFilter)
            GenericLookupFieldFilter.factory('name__istartswith', can_negate=False, negated=True),
            ("age", NumberFilter),
        )



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
