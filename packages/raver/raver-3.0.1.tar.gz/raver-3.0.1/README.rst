#####
Raver
#####

Ratio versioning checker.


**********
Quickstart
**********


Installation
============

Raver can be installed using ``pip install raver`` for any Python version >=3.9. Or, for
Poetry managed projects, use ``poetry add -D raver`` to add it as a development
dependency.


Using raver
===========

To just check if Raver can fetch and check your current version, use ``raver`` in your
favorite terminal while in your project directory (where ``pyproject.toml`` is).

Raver detects any Python module that is set up using Poetry by default. It will then
check if the version in the module/package's main file contains a ``__version__ = "..."``
line that matches the version in your ``pyproject.toml`` file.


Check w.r.t. git reference
--------------------------

To check the current version versus a git branch as reference (e.g. ``origin/master``),
use:

``raver --ref origin/master``

where ``origin/master`` is the reference branch. It then performs a comparison using
``git diff`` to check for committed changes. ``-r`` works as well as a shorthand.


Check changelog
---------------

To check whether a changelog entry exists for the current version. There are two
supported changelog methods, file and directory.

``raver --changelog ./path/to/changelog.rst``

where the changelog file can be of any extension. Raver checks whether the earlier
detected Python file version (only ``{major}.{minor}.{patch}``, no metadata) is included
in the document.

``raver --changelog ./path/to/changelog/``

is also allowed, where the changelog directory has to contain an entry in the format of
``v{major}.{minor}.{patch}*`` of the current version (the star is a glob wildcard).


TOML configuration
------------------

Raver supports TOML configuration! It **takes precedence over** any command-line
parameters. The following would be a sensible default for raver:

.. code-block:: toml

   [tool.raver]
   module = "raver"  # Change to your package name or remove to use Poetry's entry.
   reference = "origin/master"
   changelog = "./doc/source/changelog.rst"
   debug = false


***************
Developer guide
***************


Python packaging information
============================

This project is packaged using `poetry <https://python-poetry.org/>`_. Packaging
information as well as dependencies are stored in `pyproject.toml <./pyproject.toml>`_.

Installing the project and its development dependencies can be done using ``poetry install``.


Invoke tasks
============

Most elemental maintenance tasks can be accomplished using
[Invoke](https://www.pyinvoke.org/). After installing using ``poetry install`` and
enabling the environment using ``poetry shell``, you can run all tasks using ``inv
[taskname]`` or ``invoke [taskname]``. E.g. ``inv docs`` builds the documentation.


Versioning
==========

This project uses `semantic versioning <https://semver.org>`_. Version increments are
checked using `Raver <https://gitlab.com/ratio-case/raver>`_.


Changelog
=========

Changelog format as described by https://keepachangelog.com/ has been adopted.
