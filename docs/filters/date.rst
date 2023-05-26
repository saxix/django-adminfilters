.. include:: ../globals.rst

.. _filters_number:

===============
DateRangeFilter
===============

Filter dates. It allows complex filter like:


.. list-table:: Operators
   :widths: 30 70


   * - 2000-01-01
     - equals 2000-01-01
   * - =2000-01-01
     - equals 2000-01-01
   * - > 2000-01-03
     - greater than 2000-01-03
   * - < 2000-01-03
     - lower than 2000-01-03
   * - >= 2000-01-03
     - greater or equal than 2000-01-03
   * - >= 2000-01-03
     - lower or equal than 2000-01-03
   * - 2000-01-02..2000-12-02
     - betwenen 2000-01-02 and 2000-12-02
   * - <> 2000-01-02
     - not equal to 2000-01-02
   * - 2000-01-01,2000-02-01,2000-03-01
     - list of values
