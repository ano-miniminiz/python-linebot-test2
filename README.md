# OpenHackU_2020_15

## 焼肉焼いたら家焼けたbot用のリポジトリ

・このbotは、ヤフー主催の学生ハッカソン「Open Hack U 2020 Online vol.4」にて企画・開発されました。

・[遊び方](https://note.com/roast_official/n/ndc7d00f38d44)

<br>

## 実行環境

・Windows10

・Python3.9.0

<br>

## 事前準備

・[ここ](https://developers.line.biz/ja/services/messaging-api/)
からLine Developersに登録する

・Line Developersトップ>プロバイダー>アプリ名>Messaging API設定に移動して「Webhook設定」「LINE公式アカウント機能」という欄があることを確認しておく

・[ここ](https://id.heroku.com/login)
からHerokuにサインアップする

<br>

## Flaskとline-bot-sdkのインストール

・以下のコードをコマンドプロンプトで実行する

```
$ pip3 install flask
$ pip3 install line-bot-sdk
```

<br>

## 実際のコード

・[公式のSDK](https://github.com/line/line-bot-sdk-python)
にもコードはあるが、今回は
[このサイト](https://uepon.hatenadiary.com/entry/2018/07/27/002843)
を参考にmain.pyを作成する

```
from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
```

<br>

## HerokuCLIのダウンロード、アプリケーションの登録

・[このサイト](https://note.com/on_bass/n/n0495484a2b2b#TBpF9)
(Heroku Dev Centerに行く～Herokuアプリの作成)を参考にherokuのアプリケーション登録を行う

・アプリケーション名でエラーが出たとき
```
$ heroku create
$ heroku rename 新しいアプリ名 --app 古いアプリ名
```

<br>

## 環境変数の設定

(ダブルクォーテーションと大かっこは取り除く)

```
$ heroku config:set YOUR_CHANNEL_SECRET="Channel Secretの文字列" --app {自分のアプリ名}
$ heroku config:set YOUR_CHANNEL_ACCESS_TOKEN="アクセストークンの文字列" --app {自分のアプリ名}
```
・設定の確認をするとき
```
$ heroku config --app {自分のアプリ名}
```

<br>

## その他設定ファイルの作成

・python、flask、line-bot-sdkのバージョンを確認する
```
$ pip list
```
・main.pyと同じディレクトリに以下3つのファイルを作成

－runtime.txt

```
python-3.9.0
```
－requirements.txt

(のちにpandas等ライブラリを利用する場合はここに追加する)
```
Flask==1.1.2
line-bot-sdk==1.19.0
```

－Procfile(拡張子なし)
```
web: python main.py
```
・エディタから拡張子なしファイルが作成できない場合はコマンドプロンプトから作成(/作業ディレクトリ)
```
$ echo web:python main.py > Procfile
```

<br>

## Webhookの設定

・事前準備の際に確認したWebhook設定欄にある、Webhook URLを編集する

Webhook URL : `https://herokuのアプリケーション名.herokuapp.com/callback`

・LINE公式アカウント機能欄にある「応答メッセージ」の編集リンクをクリックして、応答設定を変更する(任意)

応答モード：Bot

あいさつメッセージ：オフ

応答メッセージ：オフ

Webhook：オン

<br>

## Herokuデプロイ

・コマンドプロンプト
```
$ git init
$ heroku git:remote -a herokuアプリ名
$ git add .
$ git commit -m "first commit"
$ git push heroku main
```

・2回目以降
```
$ git add .
$ git commit -m "make it better"
$ git push heroku main
```

<br>

## 参考

・[Python + HerokuでLINE BOTを作ってみた](https://qiita.com/shimajiri/items/cf7ccf69d184fdb2fb26)

・[Herokuで「Error: Missing required flag」が出る場合](https://blog.tanebox.com/archives/630/)

・[【Heroku】デプロイ後にcode=H14 desc="No web processes running"が発生する場合はProcfileを作成して対処すればOK](https://qiita.com/yagi_eng/items/9308b680e6ee41ab1d6d)

・[git push時のerror: src refspec master does not match anyについて](https://deepblue-ts.co.jp/git/git-push-error/)

・[【Git】fatal: not a git repository (or any of the parent directories): .git って怒られた【大体そんなもん】](https://daitaisonnamon.hatenablog.jp/entry/2019/10/31/235446)