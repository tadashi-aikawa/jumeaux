Jumeaux
*******

|pypi| |travis| |coverage| |complexity| |versions| |license|

.. image:: ./logo.png
   :height: 400px
   :width: 400px


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

### Create and activate env

.. sourcecode::

    $ pipenv install -d
    $ pipenv shell

### Run

.. sourcecode::

    $ python jumeaux/executor.py <args>

### Serve docs

.. sourcecode::

    $ make serve-docs

### Unite test

.. sourcecode::

    $ make test

### Integration test

.. sourcecode::

    $ make test-cli


Version up
----------

There are 2 steps.

### Update release note (mkdocs/ja/releases/index.md)

.. sourcecode::

    $ make edit-release

### Confirm that your branch name equals release version

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
