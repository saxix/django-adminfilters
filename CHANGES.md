Release 2.4
=================
* Django 5.x support


Release 2.3.1
===============
* Bug fixes


Release 2.3
=============
* BUG FIX: fixes check() implementation
* new LinkedAutoCompleteFilter


Release 2.2
=============
* Improves support for JsonFields (use `#` to cast integer `.` to cast float)


Release 2.1
=============
* add DateRangeFilter
* removes `default_app_config`
* Merge #27 - Foreign Key can refer not only to pk field (@ef-end-y)


Release 2.0.4
=============
* fixes `cast_value()` to properly handle Date/DateTime lookups


Release 2.0.3
=============
* drop support Django<3
* Fix dark mode CSS
* Improves error handling in NumberFilter/ValueFilter
* Fix AutoCompleteFilter reverse url
* fixes QueryStringFilter fk null filtering


Release 2.0.2
=============
* fixes QueryStringFilter fk null filtering


Release 2.0.1
=============
* fixes packaging


Release 2.0
===========
* add ability to save/retrieve filters configuration.
* new DjangoLookupFilter
* new QueryStringFilter


Release 1.9
===========
* Drop support Django < 3
* new JsonFieldFilter
* MultiValueTextFilter/TextFilter refactoring
* AdminFiltersMixin to easily add media files


Release 1.8
=============
* added support to Dj4
* add MultiValueTextFilter


Release 1.7
=============
* Improves AutocompleteFilter to work with chained ForeignKey


Release 1.6.1
=============
* renamed MaxMiFilter as NumberFilter
* minor improvements


Release 1.6
=============
* new `BooleanRadioFilter`
* new operators for `MaxMinFilter`. Now supports (=1; >1; >=1; <1; <=1; <>1; 1,2,3;)

Release 1.5.1
=============
* bug fixes

Release 1.5
=============
* bug fixes

Release 1.4.1
=============
* bug fixes

Release 1.4
=============
* Support Django 3.2


Release 1.3.3
=============
* Add AutoCompleteFilter


Release 1.3.2
=============
* add MaxMinFilter


Release 1.3.1
=============
* add ChoicesFieldComboFilter, ChoicesFieldRadioFilter


Release 1.3
===========
* add TextFieldFilter
* drop support for python < 3.x


Release 1.2
===========
* drop support for django < 2.1
* add support for django 3.1
* bug fixes


Release 1.1
===========
* add support for django 2.1
* updates filters templates


Release 1.0
===========
* add support for django 2.0
* new `ForeignKeyFieldFilter`
* drop support Django < 1.11


Release 0.3.1
=============
* add support for django 1.10
* fix empty variable in templates
* fixes :ghissue:`8` Fix filter id in templates


Release 0.3
===========
* django versions 1.4 to 1.9
* python 2.7, 3.4, 3.5
* broaden tests - test UnionFieldListFilter and IntersectionFieldListFilter (thanks PetrDlouhy)
* Demoproject made working and transformed to testing application (thanks PetrDlouhy)
* Various filters are included in demoproject (thanks PetrDlouhy)
* Coverage with coveralls.org  (thanks PetrDlouhy)
* Readme update with actual filters  (thanks PetrDlouhy)


Release 0.2
===========
* added MultipleSelectFieldListFilter, IntersectionFieldListFilter, UnionFieldListFilter


Release 0.1
===========
* initial relaase
