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

  =======================
  Usage
  =======================

  Usage:
    gemini.py --report <report> [--threads=<threads>] [--config=<json>] <files>...

  Options:
    <files>...
    --report = <report>    Output json file
    --threads = <threads>  The number of threads in challenge [default: 1]
    --config = <json>      Configuration file(see below) [default: config.json]


  =======================
  Config file definition
  =======================

  Set following value as default if property is blank and not REQUIRED.

  {
      "one": {
          "host": "http://one",  (# REQUIRED)
          "proxy": null
      },
      "other": {
          "host": "http://other",  (# REQUIRED)
          "proxy": null
      },
      "input": {
          "format": "plain",  (see `Input format`)
          "encoding": "utf8"
      },
      "output": {
          "encoding": "utf8"
      }
  }

  =======================
  Input format
  =======================

  Correspond to following format.

  1. plain
  ---------

  "/path1?a=1&b=2"
  "/path2?c=1"
  "/path3"

  2. apache
  ---------

  000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=1" "header2=2"
  000.000.000.000 - - [30/Oct/2014:16:11:10 +0900] "GET /path2?q1=1 HTTP/1.1" 200 - "-" "Mozilla/4.0 (compatible;)" "header1=-" "header2=-"

  3. yaml
  ---------

  - path: "/path1"
    qs:
      q1:
        - v1
      q2:
        - v2
        - v3
    headers:
      key1: "header1"
      key2: "header2"
  - path: "/path2"
    qs:
      q1:
        - v1
  - path: "/path3"
    headers:
      key1: "header1"
      key2: "header2"
  - path: "/path4"

  4. csv
  ---------

  "/path1","a=1&b=2","header1=1&header2=2"
  "/path2","c=1"
  "/path3",,"header1=1&header2=2"
  "/path4"

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
