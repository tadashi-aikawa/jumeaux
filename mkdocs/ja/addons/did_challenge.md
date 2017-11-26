did_challenge [:fa-github:][s1]
===============================

[s1]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/did_challenge

次のchallengeに移る前に処理をします。


[:fa-github:][s2] sleep
-----------------------

[s2]: https://github.com/tadashi-aikawa/jumeaux/tree/master/jumeaux/addons/did_challenge/sleep.py

指定した時間、待機します。


### Config

#### Definitions

| Key | Type  |            Description             | Example | Default |
| --- | ----- | ---------------------------------- | ------- | ------- |
| min | float | 待機時間 :fa-info-circle: の下限値 | 0.1     |         |
| max | float | 待機時間 :fa-info-circle: の上限値 | 1.0     |         |

!!! info "待機時間について"

    待機時間は`min`から`max`の範囲でランダムに決定されます。
    固定値にしたい場合は`min`と`max`に指定したい値を設定してください。

#### Examples

##### ランダムで0.1～1.0秒待機する

```yml
did_challenge:
  - name: sleep
    config:
      min: 0.1
      max: 1.0
```

##### 0.5秒待機する

```yml
did_challenge:
  - name: sleep
    config:
      min: 0.5
      max: 0.5
```
