Jumeaux
=======

[![travis](https://api.travis-ci.org/tadashi-aikawa/jumeaux.svg?branch=master)](https://travis-ci.org/tadashi-aikawa/jumeaux/builds)
[![coverage](https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/coverage.svg)](https://codeclimate.com/github/tadashi-aikawa/jumeaux/coverage)
[![complexity](https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/gpa.svg)](https://codeclimate.com/github/tadashi-aikawa/jumeaux)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
[![pypi](https://img.shields.io/pypi/v/jumeaux.svg)]()
[![versions](https://img.shields.io/pypi/pyversions/jumeaux.svg)]()

<img src="https://github.com/tadashi-aikawa/jumeaux/blob/master/logo.png?raw=true" width=400 height=400 />

Check difference between two responses of API.


Requirement
-----------

* Python3.6 (Maybe Python 3.7 is also fine)


Documentation
-------------

https://tadashi-aikawa.github.io/jumeaux/


Test Result
-----------

* Master: [![](https://api.travis-ci.org/tadashi-aikawa/jumeaux.png?branch=master)](https://travis-ci.org/tadashi-aikawa/jumeaux)
* Current [![](https://api.travis-ci.org/tadashi-aikawa/jumeaux.png?)](https://travis-ci.org/tadashi-aikawa/jumeaux)


For developer
-------------

### Requirements

* pipenv
* make

### Commands

#### Create and activate env

```
$ pipenv install -d
$ pipenv shell
```

#### Run

```
$ python jumeaux/executor.py <args>
```

#### Serve docs

```
$ make serve-docs
```

#### Unite test

```
$ make test
```

#### Integration test

```
$ make test-cli
```


### Version up

There are 2 steps.

#### Update release note (mkdocs/ja/releases/index.md)

```
$ make edit-release
```

#### Confirm that your branch name equals release version

```
$ make release
```

Finally, create pull request and merge to master!!


Licence
-------

### MIT

This software is released under the MIT License, see LICENSE.txt.

