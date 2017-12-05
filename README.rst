Jumeaux
*******

|pypi| |travis| |coverage| |complexity| |versions| |license|

.. raw:: html

   <img src="./logo.png" width=400 height=400 />

Check difference between two responses of API.


Outline
=======

.. contents::


Requirement
===========

* Python3.6 and uppper


Documentation
=============

https://tadashi-aikawa.github.io/jumeaux/


Test Result
===========

Master
------

.. image:: https://api.travis-ci.org/tadashi-aikawa/jumeaux.png?branch=master
    :target: https://travis-ci.org/tadashi-aikawa/jumeaux

Current
-------

.. image:: https://api.travis-ci.org/tadashi-aikawa/jumeaux.png?
    :target: https://travis-ci.org/tadashi-aikawa/jumeaux


For developer
=============

Commands
--------

.. sourcecode::

    # Create env
    $ pipenv install --dev --skip-lock
    # Check
    $ pipenv run python jumeaux/executor.py --help

    # Build documentation and run server locally
    $ pipenv run mkdocs serve
    # Build documentation (then you can deploy by git push)
    $ pipenv run mkdocs build


Version up
----------

1. Update master to current by `git checkout master && git pull`
2. Increment a version in `jumeaux/__init__.py`
3. Increment a version in `Dockerfile`
4. Build documentation by `mkdocs build`
5. Tags by `git tag x.y.z -m x.y.z`
6. Staging and commit
7. `git push`

TODO: automation


Licence
=======

MIT
---

This software is released under the MIT License, see LICENSE.txt.


.. |travis| image:: https://api.travis-ci.org/tadashi-aikawa/jumeaux.svg?branch=master
    :target: https://travis-ci.org/tadashi-aikawa/jumeaux/builds
    :alt: Build Status
.. |coverage| image:: https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/coverage.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/jumeaux/coverage
    :alt: Test Coverage
.. |complexity| image:: https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/gpa.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/jumeaux
    :alt: Code Climate
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
.. |pypi| image:: https://img.shields.io/pypi/v/jumeaux.svg
.. |versions| image:: https://img.shields.io/pypi/pyversions/jumeaux.svg
