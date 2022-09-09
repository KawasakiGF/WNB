import requests
import os
import json
import urllib.request
from bs4 import BeautifulSoup

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

# アプリケーションの名前となる文字列
# ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になる
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

#環境変数を実用的な変数に代入しているかも
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

url="https://weather.tsukumijima.net/api/forecast/city/300010"
response=requests.get(url)
jsonData=response.json()

#天気データ取得
date=jsonData["forecasts"][1]["date"]
weather=jsonData["forecasts"][1]["telop"]
tempMAX=jsonData["forecasts"][1]["temperature"]["max"]["celsius"]
tempMIN=jsonData["forecasts"][1]["temperature"]["min"]["celsius"]
amCOR=jsonData["forecasts"][1]["chanceOfRain"]["T06_12"]
pmCOR=jsonData["forecasts"][1]["chanceOfRain"]["T12_18"] 
#天気データ取得

tenkiInfo = '＜日付＞:{0}\n＜天気＞:{1}\n＜気温＞\n最低気温:{2}℃\n最高気温:{3}℃\n＜降水確率＞\n午前:{4}　午後{5}'.format(date,weather,tempMIN,tempMAX,amCOR,pmCOR)
tempMEAN=(int(tempMAX)+int(tempMIN))/2.0-1.0

#服装判定
if tempMEAN<=5:
    fukusou = '＜今日の服装＞\n重ね着をし、もふもふのコートやダウンジャケットの着用をするほか、手袋やマフラー、暖かい靴下など、できる限り暖かい服装選びをしましょう。'
elif tempMEAN<=9:
    fukusou = '＜今日の服装＞\n重ね着をし、ダウンコートやジャケットを着用しましょう。風が強いときは手袋やマフラーがあると安心です。'
elif tempMEAN<=13:
    fukusou = '＜今日の服装＞\nジャケットやコートなど、風を通さない服装にしましょう。ヒートテックがあると安心です。'
elif tempMEAN<=16 and weather == "晴れ":
    fukusou = '＜今日の服装＞\nニットやセーターにするか、風が無ければ軽い羽織りものを着るとよいでしょう。'
elif tempMEAN<=16:
    fukusou = '＜今日の服装＞\nニットやセーターでOKですが、寒く感じるときはジャケットやコートを着てもよいでしょう。'
elif tempMEAN<=19:
    fukusou = '＜今日の服装＞\n薄手のジャケットやパーカーにし、重ね着をするとよいでしょう。'
elif tempMEAN<=22:
    fukusou = '＜今日の服装＞\n着脱可能な羽織りものにし、温度に合わせて調節できるようにしましょう。'
elif tempMEAN<=24:
    fukusou = '＜今日の服装＞\n長袖が一枚あればOKです。半袖と薄い羽織りものでもよいでしょう。'
elif tempMEAN<=29:
    fukusou = '＜今日の服装＞\n半袖で過ごせそうです。長袖にして腕まくりをするのもよいでしょう。'
else:
    fukusou = '＜今日の服装＞\n半袖の涼しい服装にし、暑さ対策や熱中症対策を怠らないようにしましょう。'
#服装判定

#天気アイコン判定(変数ｍはリストPicNameで使用)
if weather=="晴れ":                                                     picUrl="https://i.ibb.co/v3Q1SzX/Sun.png"
elif weather=="晴時々曇" or weather=="晴一時曇" or weather=="晴のち曇": picUrl="https://i.ibb.co/47Zp7tf/Sun-To-Cloud.png"
elif weather=="晴時々雨" or weather=="晴一時雨" or weather=="晴のち雨": picUrl="https://i.ibb.co/w6yBmKP/Sun-To-Rain.png"
elif weather=="晴時々雪" or weather=="晴一時雪" or weather=="晴のち雪": picUrl="https://i.ibb.co/2hWsVQy/Sun-To-Snow.png"
elif weather=="曇り":                                                   picUrl="https://i.ibb.co/V32pwjv/Cloud.png"
elif weather=="曇時々晴" or weather=="曇一時晴" or weather=="曇のち晴": picUrl="https://i.ibb.co/wwc1J9P/Cloud-To-Sun.png"
elif weather=="曇時々雨" or weather=="曇一時雨" or weather=="曇のち雨": picUrl="https://i.ibb.co/mSXWrsm/Cloud-To-Rain.png"
elif weather=="曇時々雪" or weather=="曇一時雪" or weather=="曇のち雪": picUrl="https://i.ibb.co/Tv42FLY/Cloud-To-Snow.png"
elif weather=="雨":                                                     picUrl="https://i.ibb.co/5xkdS8V/Rain.png"
elif weather=="雨時々曇" or weather=="雨一時曇" or weather=="雨のち曇": picUrl="https://i.ibb.co/vPgg2nt/Rain-To-Cloud.png"
elif weather=="雨時々晴" or weather=="雨一時晴" or weather=="雨のち晴": picUrl="https://i.ibb.co/mzYX8j4/Rain-To-Sun.png"
elif weather=="雨時々雪" or weather=="雨一時雪" or weather=="雨のち雪": picUrl="https://i.ibb.co/GsMs2bN/Rain-To-Snow.png"
elif weather=="雪":                                                     picUrl="https://i.ibb.co/qrDSG2F/Snow.png"
elif weather=="雪時々曇" or weather=="雪一時曇" or weather=="雪のち曇": picUrl="https://i.ibb.co/qdftDWR/Snow-To-Cloud.png"
elif weather=="雪時々晴" or weather=="雪一時晴" or weather=="雪のち晴": picUrl="https://i.ibb.co/d4y70W9/Snow-To-Sun.png"
elif weather=="雪時々雨" or weather=="雪一時雨" or weather=="雪のち雨": picUrl="https://i.ibb.co/KqnPzr7/Snow-To-Rain.png"
elif weather=="暴風雨":                                                 picUrl="https://i.ibb.co/y6X5z5X/Typhon.png "
elif weather=="暴風雪":                                                 picUrl="https://i.ibb.co/2NMQLDS/Heavy-Snow.png"
#天気アイコン判定

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
#関数名は自由
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=tenkiInfo),
        ImageSendMessage(original_content_url=picUrl,preview_image_url=picUrl),
        TextSendMessage(text=fukusou)])
        #リプライはLineBotApiのメソッドを用いる。 第一引数のevent.reply_tokenはイベントの応答に
        #用いるトークン。 第二引数にはlinebot.modelsに定義されている返信用の
        #TextSendMessageオブジェクトを渡しています。
##############################################

#決まり文句
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)