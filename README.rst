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

Requires pipenv and make.

Commands
--------

.. sourcecode::

    # Create env
    $ make init
    # Check
    $ pipenv run python jumeaux/executor.py --help

    # Build documentation and run server locally
    $ make build-docs
    # Build documentation (then you can deploy by git push)
    $ make package-docs


Version up
----------

.. sourcecode::

    # Update release note and ADD !!!!
    $ make release version=x.y.z
    $ git push
    $ make publish version=x.y.z


Finally, create pull request and merge to master!!


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
