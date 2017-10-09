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
$ docker build -t tadashi-aikawa/jumeaux
```

### Vagrant and Virtualbox

See [Jumeaux Toolbox] .


:fa-file: Create files
----------------------

Before executing jumeaux, you need to create two files.

### config.yml

Create `config.yml` as following.

!!! summary "config.yml"

    ```yml
    title: DEMO
    one:
        name: one
        host: https://one
    other:
        name: other
        host: https://other
    output:
        response_dir: responses
    addons:
        log2reqs:
            name: jumeaux.addons.log2reqs.plain
    ```

Above is minimal configuration which can works. (It is not useable :sweat:)
So if you use jumeaux for production, see [Configuration :fa-sticky-note:](configuration.md).

### requests

Create `requests` and write paths you want to test as following

!!! summary "requests"

    ```
    /res/1.json
    /res/2.json
    ```


:fa-play-circle: Execute
------------------------

Finally, you can execute jumeaux with specifying `config.yml` and `requests`.
[Report :fa-sticky-note:](report.md) shows you what the output means


### Python3.6 and upper

```
$ jumeaux --config config.yml requests
```

### Docker

```
$ docker run -it tadashi-aikawa/jumeaux --config config.yml requests
```

### Vagrant and Virtualbox

See [Jumeaux Toolbox] .


[Jumeaux Toolbox]: https://github.com/tadashi-aikawa/jumeaux-toolbox
[todo]: todo.md
