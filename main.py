from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)
import os

# アプリケーションの名前となる文字列
# ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になる
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

#環境変数を実用的な変数に代入しているかも
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#####################通信の検証####################
# @app.route("/callback"...はappに対して/callbackというURLに対応するアクションを記述
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value 署名検証
    signature = request.headers['X-Line-Signature']

    # get request body as text リクエストボディ取得(これも検証の一環かしら)
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    # 署名検証で失敗したときは例外をあげる
    except InvalidSignatureError:
        abort(400)

    return 'OK'
###############################################

##########実行するプログラムの内容をここに書く################
#@handler.addのメソッドの引数にはイベントのモデルを入れる(MessageEvent=メッセージを受けたら)
@handler.add(MessageEvent)
def handle_image_message(event):
    url="https://1.bp.blogspot.com/-eaDZ7sDP9uY/Xhwqlve5SUI/AAAAAAABXBo/EcI2C2vim7w2WV6EYy3ap0QLirX7RPohgCNcBGAsYHQ/s400/pose_syanikamaeru_man.png"
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url=url,preview_image_url=url))

#関数名は自由
#def handle_message(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text))
        #event.message.textは送られてきた文字列かも
        #リプライはLineBotApiのメソッドを用いる。 第一引数のevent.reply_tokenはイベントの応答に
        #用いるトークン。 第二引数にはlinebot.modelsに定義されている返信用の
        #TextSendMessageオブジェクトを渡しています。
#@handler.add(MessageEvent, message=TextMessage)
##############################################

#決まり文句
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)