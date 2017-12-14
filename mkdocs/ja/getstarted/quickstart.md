Quickstart
==========

:fa-desktop: Requirements
-------------------------

以下の環境いずれかが必要です。

* Python3.6以上(推奨)
* Docker
* VagrantとVirtualbox


:fa-download: Installation
--------------------------

### Python3.6以上(推奨)

```
$ pip install jumeaux
```

`jumeaux --version`でバージョンが表示されればOKです。

### Docker

```
$ git clone https://github.com/tadashi-aikawa/jumeaux.git
$ cd jumeaux
$ docker build -t tadashi-aikawa/jumeaux .
```

`docker run -it tadashi-aikawa/jumeaux --version`でバージョンが表示されればOKです。

!!! warning

    以降はPythonの場合を想定して説明します。
    つまり `jumeaux` => `docker run -v (pwd):/tmp -it tadashi-aikawa/jumeaux` とコマンドを置き換えてください。

### VagrantとVirtualbox

[Jumeaux Toolbox]はJumeauxを利用する環境一式を作成/利用することができます。  
その中にJumeauxも含まれるため、それを使用することができます。

!!! warning

    サンドボックス環境以外での使用はあまりおすすめしません。


:fa-file: Create files
----------------------

Jumeauxを実行するには、以下2つのファイルを用意する必要があります。

| ファイル名 |              役割              |              備考               |
| ---------- | ------------------------------ | ------------------------------- |
| config.yml | 設定ファイル                   | 任意のファイルを1つ以上指定可能 |
| requests   | リクエストが記載されたファイル | 任意のファイルを1つ以上指定可能 |

上記ファイルの作成に`jumeaux init`コマンドを使用できます。

```
$ jumeaux init minimum
```

`minimum`は作成するファイルの種類です。

!!! note

    `jumeaux init help`コマンドで`minimum`以外の有効な値を確認できます。


:fa-play-circle: Execute
------------------------

`config.yml`と`requests`を指定して実行しましょう。
出力結果の意味は[Report :fa-sticky-note:](report.md)をご覧ください。

```
$ jumeaux run requests
```

!!! note

    `--config`を指定しないと`config.yml`が設定されたことになります。
    つまり、`jumeaux run requests`は以下のコマンドと等価です。
    
    ```
    $ jumeaux run requests --config config.yml
    ```


[Jumeaux Toolbox]: https://github.com/tadashi-aikawa/jumeaux-toolbox
[todo]: todo.md
