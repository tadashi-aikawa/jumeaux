Gemini
*****************

Check difference between two responses of API.

Outline
================

.. contents::


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
    0.5.0


Usage
=================

::

  gemini --host-one=<host_one> --host-other=<host_other> --report <report> <files>...
                        [--input-format=<input_format>]
                        [--proxy-one=<proxy_one>] [--proxy-other=<proxy_other>]
                        [--input-encoding=<input_encoding>] [--output-encoding=<output_encoding>]
                        [--threads=<threads>]

  Options:
  <files>...
  --host-one = <host_one>                   One host
  --host-other = <host_other>               Other host
  --proxy-one = <proxy_one>                 Proxy for one host
  --proxy-other = <proxy_other>             Proxy for other host
  --input-format = <input_format>           Input file format [default: apache]
  --input-encoding = <input_encoding>       Input file encoding [default: utf8]
  --output-encoding = <output_encoding>     Output json encoding [default: utf8]
  --threads = <threads>                     The number of threads in challenge [default: 1]
  --report = <report>                       Output json file

Example

.. sourcecode:: bash

    $ python gemini.py --host-one   http://one.net   \
                       --host-other http://other.net \
                       --report     report.json      \
                       access.log


Licence
=================

MIT
---------

This software is released under the MIT License, see LICENSE.txt.
