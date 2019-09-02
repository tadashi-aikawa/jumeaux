Jumeaux add-on sample
**********************

If you want to create jumeaux add-on, please use this!


Outline
=======

.. contents::


Requirement
===========

* pipenv (with python 3.7)
* make


Tutorial
========

### Create environment

.. sourcecode::

    $ make init

### Run sample add-ons

There are three add-ons from the beginning.

1. reqs2reqs/add_path (Add specified path to requests)
2. judgement/ignore_values (Ignore differences which includes values specified in config)
3. final/table (Output report as table)

#### Edit config.yml

Add to a `addons` section in config.yml

.. sourcecode::

    reqs2reqs:
      - name: addon_sample.reqs2reqs.add_path
        config:
          path: /hogehoge

    # Don't replace but add below
    judgement:
      - name: addon_sample.judgement.ignore_values
        config:
          values:
            - apple
            - orange

    final:
      - name: addon_sample.final.table
        config:
          columns:
            - seq
            - name
            - path
            - status

#### Run jumeaux

.. sourcecode::

    $ make run ARGS="requests -v"

### Edit or create your add-ons!!

TODO

### Edit setup.py

You need to change `addon_sample` to your package name.

.. sourcecode::

  setup(
      name='addon_sample',


Licence
=======

MIT
---

This software is released under the MIT License, see LICENSE.txt.

