Jumeaux
=======

[![pypi](https://img.shields.io/pypi/v/jumeaux.svg)](https://pypi.org/project/jumeaux/)
[![Versions](https://img.shields.io/pypi/pyversions/jumeaux.svg)](https://pypi.org/project/jumeaux/)
[![Actions Status](https://github.com/tadashi-aikawa/jumeaux/workflows/Tests/badge.svg)](https://github.com/tadashi-aikawa/jumeaux/actions)
[![codecov](https://codecov.io/gh/tadashi-aikawa/jumeaux/branch/master/graph/badge.svg)](https://codecov.io/gh/tadashi-aikawa/jumeaux)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tadashi-aikawa/jumeaux/blob/master/LICENSE)

<img src="https://github.com/tadashi-aikawa/jumeaux/blob/master/logo.png?raw=true" width=400 height=400 />

Check difference between two responses of API.


🎥 Demo
---------

See [Top page in documentation](https://tadashi-aikawa.github.io/jumeaux/)


🦉 Install
------------

See [quick start in documentation](https://tadashi-aikawa.github.io/jumeaux/ja/getstarted/quickstart/).


💻 For developer
------------------

### Requirements

* poetry
* make

### Flow

1. Development on master and if you need branches and issues, create them
2. Commit with prefix emoji such as "📝", and suffix issue number like "#120"

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
$ make test-e2e
```



📦 Release
------------

### Requirements

* **Windows is not supported!!!**
* poetry
* make

### Update release note (mkdocs/ja/releases/*)

```
$ git commit -m "📝 Update release note"
$ git push
```

### Commands

```bash
make release version=x.y.z
```

🎫 Licence
------------

### MIT

This software is released under the MIT License, see LICENSE.txt.

