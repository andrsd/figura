Export
======

Currently models can be exported into 2 file formats:

- STEP
- STL

API
---

Exporting via API is done by ``export`` function:

.. card:: Export into a file

   .. code::

      export(<file_name>, <list of objects>, [file_format])

   The ``file_format`` parameter is optional and its default value is ``step``.


Command-line
------------

Exporting via command line execution is done via ``export`` variable.

.. card:: Export

   .. code::

      export = [<list of objects>]

Special variable ``export`` is reserved for exporting into files when using the command-line
approach.
