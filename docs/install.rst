.. include:: globals.rst

.. _install:

============
Installation
============

Installing django-adminfilters is as simple as checking out the source and adding it to
your project or ``PYTHONPATH``.


1. First of all follow the instruction to install `django_admin`_ application,

2. Either check out django-adminfilters from `GitHub`_ or to pull a release off `PyPI`_. Doing ``pip install django-adminfilters`` or ``easy_install django-adminfilters`` is all that should be required.

3. Either symlink the ``adminfilters`` directory into your project or copy the directory in. What ever works best for you.


Install test dependencies
=========================

If you want to run :mod:`adminfilters` tests you need extra requirements


.. code-block:: python

    pip install -U django-adminfilters


Configuration
=============

Add :mod:`adminfilters` to your `INSTALLED_APPS`::

    INSTALLED_APPS = (
        'adminfilters',
        ...
    )
