Template
========

一部の設定ではjinja2形式のテンプレート表現を受けつけます。  
対応内容の詳細は[jinja2公式サイト](http://jinja.pocoo.org/docs/2.10/templates/)をご覧下さい。


:fa-pencil: Property rules
--------------------------

条件を記載するwhenプロパティと、値を記載するその他プロパティで記載の仕方が少し異なります。


### when系プロパティ

`when`だけでなく`when_any`や`when_all`も対象に含まれます。

* 条件式を記載
* 全てが式であるため`{{ }}`で囲まない
* 文字列はクォートで囲む

Typeが[Trial][trial]であるtrial変数を使った場合の一例です。

`OK`

```
- when: "trial.name == 'json'"
```

`NG`

```
- when: "trial.name == json"
```

```
- when: "{{ trial.name == json }}"
```


### when系以外のプロパティ

* 値の一部として記載
* 基本は値であるためテンプレート部分は`{{ }}`で囲む
* 文字列はクォートで囲まない
    * ただし、条件式などで利用するテンプレート内の文字列は囲む必要あり

Typeが[Trial][trial]であるtrial変数を使った場合の一例です。  
プロパティ名はtagです。

`OK`

```
- tag: "TAG: {{ trial.name }}"
```

```
- tag: "{{ trial.name == 'hoge' }}"
```

`NG`

```
- when: "TAG: trial.name"
```

```
- when: "trial.name == hoge"
```

```
- when: "{{ trial.name == hoge }}"
```


:fa-filter: Filters
-------------------

JumeauxオリジナルのFilterをいくつか利用できます。


### reg(regstr)

正規表現に完全一致する場合はTrueを返します。

#### Examples

年齢(age)が2桁がどうか

`age|reg("[0-9]{2}")`


:fa-calculator: Functions
-------------------------

Jumeauxオリジナルの関数をいくつか利用できます。


### calc_distance_km(lat1: float, lon1: float, lat2: float, lon2: float)

座標(lat1, lon1)～座標(lat2, lon2)間の概算距離を計算します。

* 測地系はWGS84
* 単位はdegree
* 返却値は浮動小数点
* 返却値の単位はkm

#### Examples

```python
calc_distance_km(35.694253, 139.784099, 35.664131, 139.759302)
```

### equals_without_host(one: str, other: str)

文字列oneとotherについて、ホスト部分を除き一致するかどうかを判定します。

#### Examples

```python
equals_without_host("https://hoge.com/hoge", "https://fuga.com/hoge")
// -> True
equals_without_host("https://hoge.com/hoge", "https://hoge.com/fuga")
// -> False
```

[trial]: ./models/trial

