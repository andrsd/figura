Installation
============

Requirements:

* pythonocc-core (>=7.6.0)
* multimethod (>=1.9.0)


.. tab-set::

   .. tab-item:: conda

      1. Add the following channels:

         .. code::

            $ conda config --add channels conda-forge
            $ conda config --add channels andrsd

      2. Install

         .. code::

            $ conda install -c andrsd figura

   .. tab-item:: pip

      Unfortunately `pythonocc-core` is only available via `conda-forge` so you won't be able to use pip-only install.
      You can see the `discussion about the package deployment <https://github.com/tpaviot/pythonocc-core/issues/667>`_.

      1. Use conda environment with conda-forge:

         .. code::

            $ conda config --add channels conda-forge
            $ conda config --set channel_priority strict
            $ conda install pythonocc-core

      2. Install figura from source:

         .. code::

            $ cd /some/path
            $ git clone https://github.com/andrsd/figura.git
            $ cd figura
            $ pip install .
