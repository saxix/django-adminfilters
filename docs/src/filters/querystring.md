[//]: # (# QueryString)

## QueryStringFilter

[//]: # (![querystring]&#40;../static/images/querystring.gif&#41;{width=400})


Allows complex filtering criteria, each line represent a ``field/value`` filter entry.
Each line can be negated using ``!`` prefix


### Usage


    class MyModelAdmin(AdminFiltersMixin, models.ModelAdmin):
        list_filter = (
            QueryStringFilter,
            ...
            )

### Options


.. attribute:: QueryStringFilter.can_negate

    Control ability to work as `exclude` filter. Set to `False` hides the Exclude checkbox

.. attribute:: QueryStringFilter.placeholder

    Placeholder value for the Key input text. (Default. "field value")

.. attribute:: QueryStringFilter.template

    Template name used to render the filter. (Default. "adminfilters/querystring.html")

.. attribute:: QueryStringFilter.title

    Filter title. (Default. "QueryString")

### Configuration


The filter can be configured either using subclassing or `.factory()` method::

    class MyModelAdmin(AdminFiltersMixin, models.ModelAdmin):
        list_filter = (
            QueryStringFilter.factory(title=_("Generic field filter")),
            ...
            )


### Usage Examples



    # Model.objects.filter(year=1972, name__istartswith="Annie")

    year=1972
    name__istartswith=Annie


    # Model.objects.filter(date__gt="2021-10-1").exclude(date__month=12)

    date__gt=2021-10-1
    !date__month=12
