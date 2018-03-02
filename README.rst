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

* Python3.6


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

Requirements
------------

* pipenv
* make

Commands
--------

.. sourcecode::

    # Create env
    $ make init
    # Check
    $ make run ARGS="--help"

    # Build documentation and run server locally
    $ make serve-docs
    # Build documentation (then you can deploy by git push)
    $ make package-docs


Version up
----------

Before release, you need to

1. Update release note (mkdocs/ja/releases/index.md)
2. Confirm that your branch name equals release version

Then

.. sourcecode::

    $ make release


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
