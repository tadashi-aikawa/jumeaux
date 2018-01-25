Notifier
========

通知設定の定義です。

Definitions
-----------

### Notifier

!!! danger

    本プロパティの仕様はベータ版です。  
    近いうちに破壊的変更が入る可能性があります。

|    Key     |             Type              |   Description    |           Example           | Default |
| ---------- | ----------------------------- | ---------------- | --------------------------- | ------- |
| type       | NotifierType :fa-info-circle: | 通知のタイプ     | slack                       |         |
| channel    | string                        | 通知先           | `#times_test`               |         |
| username   | (string)                      | 通知ユーザ名     | jenkins                     | jumeaux |
| icon_emoji | (string)                      | アイコンの絵文字 | smile                       |         |
| icon_url   | (string)                      | アイコンのURL    | `http://jumeaux/images.img` |         |

??? info "type"

    | Name  | Description |
    | ----- | ----------- |
    | slack | Slack       |


Examples
--------

### Slackの`#times_test`チャンネルに通知するNotifier

```yml
type: slack
channel: "#times_test"
icon_emoji: "innocent"
```
