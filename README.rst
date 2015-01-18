Gemini
*****************

Check difference between two responses of API.

Outline
================

.. contents::


Features
=================

todo


Requirement
=================

* Python3.3
   - Unsupported version of 2.X
   - Maybe, python3.4 is supported.
* Python packages
   - requests
   - docopt
   - schema
   - xmltodict
   - pyyaml


Installation
=================

Download and extract
----------------------

.. sourcecode:: bash

    $ wget 'https://github.com/tadashi-aikawa/gemini/archive/master.zip' -O master.zip
    $ unzip master.zip -x */test/*
    $ rm master.zip


Create virtual environment and activate it
---------------------------------------------

.. sourcecode:: bash

    $ cd gemini-master
    $ /usr/bin/pyvenv pyvenv
    $ source pyvenv/bin/activate


Install pip (under Python3.4 only)
---------------------------------------------

.. sourcecode:: bash

    $ curl -O https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz
    $ tar xzf distribute-0.6.49.tar.gz
    $ python distribute-0.6.49/distribute_setup.py
    $ rm -rf distribute*
    $ easy_install pip


Install requisite packages
----------------------------

.. sourcecode:: bash

    $ pip install -r requirements.txt


Check operation
----------------------------

.. sourcecode:: bash

    $ python gemini.py --version
    0.9.0


Usage
=================

::

  Usage:
    gemini --report <report> [--threads=<threads>] [--config=<json>] <files>...

  Options:
    <files>...
    --report = <report>    Output json file
    --threads = <threads>  The number of threads in challenge [default: 1]
    --config = <json>      Configuration file(see below) [default: config.json]

  Config file definition:
    # Set following value as default if property is blank and not REQUIRED.
      {
          "one": {
              "host": "http://one",  (# REQUIRED)
              "proxy": None
          },
          "other": {
              "host": "http://other",  (# REQUIRED)
              "proxy": None
          },
          "input": {
              "format": "yaml",
              "encoding": "utf8"
          },
          "output": {
              "encoding": "utf8"
          }
      }

Example

.. sourcecode:: bash

    $ python gemini.py --report report.json accesslog.yaml


Test Result
=================

Master
-----------

.. image:: https://api.travis-ci.org/tadashi-aikawa/gemini.png?branch=master
    :target: https://travis-ci.org/tadashi-aikawa/gemini

Current
-----------

.. image:: https://api.travis-ci.org/tadashi-aikawa/gemini.png?
    :target: https://travis-ci.org/tadashi-aikawa/gemini


Licence
=================

MIT
---------

This software is released under the MIT License, see LICENSE.txt.
