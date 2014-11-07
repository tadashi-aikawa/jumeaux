Gemini
*****************

Check difference between two responses of API.


Test Result
=================

.. image:: https://api.travis-ci.org/tadashi-aikawa/gemini.png?branch=master
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

Create virtual environment and activate it.

.. sourcecode:: bash

    $ /usr/bin/pyvenv pyvenv
    $ source pyvenv/bin/activate


Install pip.

.. sourcecode:: bash

    $ curl -O https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz
    $ tar xzf distribute-0.6.49.tar.gz
    $ python distribute-0.6.49/distribute_setup.py
    $ rm -rf distribute*
    $ easy_install pip
    $ cd ../

Install requisite packages.

.. sourcecode:: bash

    $ pip install -r requirements.txt

todo: Download and extract.


Usage
=================

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
