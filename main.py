from flask import Flask, request, abort
import os
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReplyButton, MessageAction, QuickReply, StickerSendMessage, FollowEvent
)

app = Flask(__name__)

#環境変数取得
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

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='おはこんにちは！\n焼肉焼いたら家焼けたbotです！\n「まんざい」って送ってみてね')
    )

# elifの部分は別クラスにするのもアリ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    language_list = ["やかましいわ！", "知らんがな", "欧米かっ！", "ちょっと何言ってるかわからない",
                     "太るって！", "病院行きな", "食べすぎだよ"]
    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}"))
             for language in language_list]

    if event.message.text in language_list:
        sticker_list = [[11537, 52002750], [11537, 52002751], [11537, 52002763],
                        [11538, 51626501], [11538, 51626506], [11538, 51626515]]
        r = random.randint(0, 5)

        # スタンプを返す
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=sticker_list[r][0], sticker_id=sticker_list[r][1]))

    elif event.message.text == "まんざい":
        # 本来はここで韻を踏んだもの(text)を受け取って送る
        messages = TextSendMessage(text="ぜんざい", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)

    else:
        # オウム返し(そのうち不要になる)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)