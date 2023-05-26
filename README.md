django-adminfilters
===================

Collection of extra filters for the Django admin site

Demo can be found at https://django-adminfilters.herokuapp.com/demo/artist/

[![Pypi](https://badge.fury.io/py/django-adminfilters.svg)](https://badge.fury.io/py/django-adminfilters)
[![coverage](https://codecov.io/github/saxix/django-adminfilters/coverage.svg?branch=develop)](https://codecov.io/github/saxix/django-adminfilters?branch=develop)
[![Test](https://github.com/saxix/django-adminfilters/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-adminfilters/actions/workflows/test.yml)
[![ReadTheDocs](https://readthedocs.org/projects/django-adminfilters/badge/?version=latest)](https://django-adminfilters.readthedocs.io/en/latest/)


https://user-images.githubusercontent.com/27282/153727131-d875f946-a8a8-4d89-be83-1d8cb5c9391a.mp4


Filters
=======

* Autocomplete
  * AutocompleteFilter
* Simple
  * ValueFilter
* Combobox
  * AllValuesComboFilter
  * RelatedFieldComboFilter
  * ChoicesFieldComboFilter
* Dates
  * DateRangeFilter
* Radio
  * AllValuesRadioFilter
  * RelatedFieldRadioFilter
  * ChoicesFieldRadioFilter
  * BooleanRadioFilter
* Checkbox
  * RelatedFieldCheckBoxFilter
* Multiple
  * MultiValueFilter
* ManyToMany
  * IntersectionFieldListFilter
  * UnionFieldListFilter
* JSON
  * JsonFieldFilter
* Number
  * NumberFilter
* Special
  * QueryStringFilter
  * DjangoLookupFilter
  * PermissionPrefixFilter

FYI
====

Filters management (save/retrieve), is handled by an optional application `adminfilters.depot` that,
due to the Django filters internal design, it uses GET method to save filter definition to the database.
When you use `FilterDepotManager` to save a filter, the call is *idempotent* but not *safe*.


Usage examples
==============


    class MyModel(models.Model):
        index = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
        age = models.IntegerField()
        flag = models.CharField(default="1", choices=(("0", "Flag 1"), ("1", "Flag 2"))
        household = models.ForeignKey('Household')
        custom = JSONField(default=dict, blank=True)

    class MyModelAdmin(ModelAdmin):
        list_filter = (
            FilterDepotManager,  # needs `adminfilters.depot` app
            QueryStringFilter,
            DjangoLookupFilter,
            ("custom", JsonFieldFilter.factory(can_negate=False, options=True)),
            ("flag", ChoicesFieldComboFilter),
            ('household', AutoCompleteFilter)
            ('name', ValueFilter.factory(lookup='istartswith'),
            ("age", NumberFilter),
        )



Run demo app
============

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
* Documentation: https://django-adminfilters.readthedocs.io/en/latest/
