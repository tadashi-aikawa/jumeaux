Jumeaux
=======

[![Versions](https://img.shields.io/pypi/pyversions/jumeaux.svg)](https://pypi.org/project/jumeaux/)
[![pypi](https://img.shields.io/pypi/v/jumeaux.svg)](https://pypi.org/project/jumeaux/)
[![Actions Status](https://github.com/tadashi-aikawa/jumeaux/workflows/Tests/badge.svg)](https://github.com/tadashi-aikawa/jumeaux/actions)
[![coverage](https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/coverage.svg)](https://codeclimate.com/github/tadashi-aikawa/jumeaux/coverage)
[![complexity](https://codeclimate.com/github/tadashi-aikawa/jumeaux/badges/gpa.svg)](https://codeclimate.com/github/tadashi-aikawa/jumeaux)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tadashi-aikawa/jumeaux/blob/master/LICENSE)

<img src="https://github.com/tadashi-aikawa/jumeaux/blob/master/logo.png?raw=true" width=400 height=400 />

Check difference between two responses of API.


Demo
----

See [Top page in documentation](https://tadashi-aikawa.github.io/jumeaux/)


Install
-------

See [quick start in documentation](https://tadashi-aikawa.github.io/jumeaux/ja/getstarted/quickstart/).


For developer
-------------

### Requirements

* poetry
* make

### Flow

1. Create new version as following
  * branch like as 2.3.0
  * GitHub projects like as 2.3.0
2. Create Issue and development! (Feature branch is optional. It likes as Issue-120)
3. Commit with prefix emoji like ":memo:", and suffix issue number like "#120"


### Commands

#### Create environment

```
$ poetry env use <path of python 3.8>
$ poetry install
```

#### Run

```
$ poetry run jumeaux <args>
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

**Windows is not supported!!!**

There are 2 steps.

#### Update release note (mkdocs/ja/releases/*)

```
$ git commit -m "📝 Update release note"
$ git push
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

