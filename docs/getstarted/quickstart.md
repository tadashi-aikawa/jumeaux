Quickstart
==========

:fa-desktop: Requirements
-------------------------

It is necessary to satisfy one of the following.

* Python3.6 and upper
* Docker
* Vagrant and Virtualbox


:fa-download: Installation
--------------------------

### Python3.6 and upper

```
$ pip install jumeaux
$ jumeaux --version
```

### Docker

```
$ docker build -t tadashi-aikawa/jumeaux .
$ docker run -it tadashi-aikawa/jumeaux --version
```

!!! warning

    After that, please complement python case to docker command.
    It means `jumeaux` => `docker run -it tadashi-aikawa/jumeaux`.

### Vagrant and Virtualbox

See [Jumeaux Toolbox] .


:fa-file: Create files
----------------------

Before executing jumeaux, you need to create two files.

* config.yml
* requests

You can create these files by using below command.

```
$ jumeaux init minimum
```

!!! note

    `jumeaux init help` shows all targets.


:fa-play-circle: Execute
------------------------

Finally, you can execute jumeaux with specifying `config.yml` and `requests`.
[Report :fa-sticky-note:](report.md) shows you what the output means

```
$ jumeaux requests
```

!!! note

    Default value of `--config` is `config.yml`.
    So `jumeaux requests` equals below actually.
    
    ```
    $ jumeaux --config config.yml requests
    ```


[Jumeaux Toolbox]: https://github.com/tadashi-aikawa/jumeaux-toolbox
[todo]: todo.md
