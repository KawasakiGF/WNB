import re
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

#対話内容を管理するクラスとインスタンスの初期設定
class Status:
    def __init__(self):
          self.context = ""
          self.date = 0
          self.area = ""
          self.areaT = ""
          self.basyoList = ""

    def get_context(self):
        return self.context
    def set_context(self, context):
          self.context = context

    def get_date(self):
        return self.date
    def set_date(self, date):
          self.date = date

    def get_area(self):
        return self.area
    def set_area(self, area):
          self.area = area

    def get_areaT(self):
        return self.areaT
    def set_areaT(self, areaT):
          self.areaT = areaT

    def get_basyoList(self):
        return self.basyoList
    def set_basyoList(self, basyoList):
          self.basyoList = basyoList


class MySession:
    _status_map = dict()

    def register(user_id):
        if MySession._get_status(user_id) is None:
            MySession._put_status(user_id, Status())

    def reset(user_id):
        MySession._put_status(user_id, Status())

    def _get_status(user_id):
        return MySession._status_map.get(user_id)
    def _put_status(user_id, status: Status):
        MySession._status_map[user_id]= status

    def read_context(user_id):
        return MySession._status_map.get(user_id).get_context()
    def update_context(user_id, context):
        new_status = MySession._status_map.get(user_id)
        new_status.set_context(context)
        MySession._status_map[user_id] = new_status

    def read_date(user_id):
        return MySession._status_map.get(user_id).get_date()
    def update_date(user_id, date):
        new_status = MySession._status_map.get(user_id)
        new_status.set_date(date)
        MySession._status_map[user_id] = new_status

    def read_area(user_id):
        return MySession._status_map.get(user_id).get_area()
    def update_area(user_id, area):
        new_status = MySession._status_map.get(user_id)
        new_status.set_area(area)
        MySession._status_map[user_id] = new_status

    def read_areaT(user_id):
        return MySession._status_map.get(user_id).get_areaT()
    def update_areaT(user_id, areaT):
        new_status = MySession._status_map.get(user_id)
        new_status.set_areaT(areaT)
        MySession._status_map[user_id] = new_status

    def read_basyoList(user_id):
        return MySession._status_map.get(user_id).get_basyoList()
    def update_basyoList(user_id, basyoList):
        new_status = MySession._status_map.get(user_id)
        new_status.set_basyoList(basyoList)
        MySession._status_map[user_id] = new_status

#都道府県コードを返す
def todoufukenNum(num):
     if num < 10:
          return "0" + str(num)
     else: return str(num)

#都道府県の場所コード探す
def codeKaraFind(finder):
     teijiBasyoList = ""
     for i in range(0, len(Tcode)):
          if re.match((finder + "...."), Tcode[i]):
               teijiBasyoList += "\n ・" + Tname[i]

     return teijiBasyoList
      
#天気メッセージを作る
def OtenkiMessageMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     date=jsonData["forecasts"][itu]["date"]
     weather=jsonData["forecasts"][itu]["telop"]
     tempMAX=jsonData["forecasts"][itu]["temperature"]["max"]["celsius"]
     tempMIN=jsonData["forecasts"][itu]["temperature"]["min"]["celsius"]
     amCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T06_12"]
     pmCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T12_18"] 
     #天気メッセージ作成
     tenkiInfo = '＜日付＞:{0}\n＜天気＞:{1}\n＜気温＞\n最低気温:{2}℃\n最高気温:{3}℃\n＜降水確率＞\n午前:{4}　午後{5}'.format(date,weather,tempMIN,tempMAX,amCOR,pmCOR)
     tempMEAN=(int(tempMAX)+int(tempMIN))/2.0-1.0


#服装判定
def fukusouHantei(tempMEAN):
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
  return fukusou

#天気アイコン判定
def picUrlMaker(weather):
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
    return picUrl


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
@handler.add(MessageEvent,message=TextMessage)
#関数名handle_messageは自由
#statusで1か所or2か所を管理。1x...1か所。2x...2か所
def handle_message(event):
    talk = event.message.text
    user_id = event.source.user_id

    MySession.register(user_id)

#会話を中断したいとき
    if (talk == "キャンセル"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("最初からやり直します。1か所or2か所を入力してください。"))
        # 現在のstatusを消して新規statusで初期化。
        MySession.reset(user_id)

#1か所の場所を聞く####################
    if MySession.read_context(user_id) == "0":
       if ("1" in talk or "１" in talk):
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDay))
          MySession.update_context(user_id, "10")
       else:
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDayError))

#日にちを聞く
    elif MySession.read_context(user_id) == "10":
       if talk in day:
           for n in range(0, len(day)):
                if talk in day[n]:
                     MySession.update_date(user_id, n)

           line_bot_api.reply_message(
           event.reply_token,
           TextSendMessage(text=day[MySession.read_date(user_id)] + tellBasyo))
           MySession.update_context(user_id, "11")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「今日」、「明日」、「明後日」の中から入力してください。"))

#1か所の場所を聞く
    elif MySession.read_context(user_id) == "11":
       if talk in todoufuken:
          MySession.update_areaT(user_id, talk)
          TBasyo = todoufukenNum(int(todoufuken.index(talk)))
          #TBasyoは文字型
          MySession.update_area(user_id, TBasyo)
          #area, basyoListは文字型
          kwsiBasyoList = codeKaraFind(MySession.read_area(user_id))
          MySession.update_basyoList(user_id, kwsiBasyoList)
          line_bot_api.reply_message(
               event.reply_token,
               [TextSendMessage(text=(talk + tellBasyoKwsk)),
                TextSendMessage(text=MySession.read_basyoList(user_id))])
          MySession.update_context(user_id, "12")

#1か所の場所の詳細を聞く&1か所の天気情報を教える
    elif MySession.read_context(user_id) == "12":
       if talk in MySession.read_basyoList(user_id):
          picUrl = picUrlMaker(OtenkiMessageMaker.weather(Tcode[Tname.index(talk)], MySession.read_date))
          fukusou = fukusouHantei(OtenkiMessageMaker.tempMEAN(Tcode[Tname.index(talk)], MySession.read_date))
          line_bot_api.reply_message(
               event.reply_token,
               [TextSendMessage(text=MySession.read_areaT + talk + checkBasyoKwsk + day[MySession.read_date] + "の" + MySession.read_areaT + talk + "の天気情報を表示します！"),
               TextSendMessage(text=OtenkiMessageMaker(Tcode[Tname.index(talk)], MySession.read_date)),
               ImageSendMessage(original_content_url=picUrl,preview_image_url=picUrl),
               TextSendMessage(text=fukusou)])
          MySession.reset(user_id)


#2か所の場所を聞く####################
    if MySession.read_context(user_id) == "0":
       if ("2" in talk or "２" in talk):
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDay))
          MySession.update_context(user_id, "20")
       else:
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDayError))

#該当しないメッセージが送られてきた場合
    else:
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text="最初からやり直します。1か所or2か所を入力してください。"))
      MySession.reset(user_id)
          #リプライはLineBotApiのメソッドを用いる。 第一引数のevent.reply_tokenはイベントの応答に
          #用いるトークン。 第二引数にはlinebot.modelsに定義されている返信用の
          #TextSendMessageオブジェクトを渡しています。
##############################################


##################その他のinfo#####################
todoufuken=["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
"茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
"新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県",
"静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
"奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県",
"徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
"熊本県","大分県","宮崎県","鹿児島県","沖縄県"]

day=["今日","明日","明後日"]

#DB使えないんだよね。。。
Tcode=['011000','012010','012020','013010','013020','013030','014010','014020','014030','015010',
'015020','016010','016020','016030','017010','017020','020010','020020','020030','030010',
'030020','030030','040010','040020','050010','050020','060010','060020','060030','060040',
'070010','070020','070030','080010','080020','090010','090020','100010','100020','110010',
'110020','110030','120010','120020','120030','130010','130020','130030','130040','140010',
'140020','150010','150020','150030','150040','160010','160020','170010','170020','180010',
'180020','190010','190020','200010','200020','200030','210010','210020','220010','220020',
'220030','220040','230010','230020','240010','240020','250010','250020','260010','260020',
'270000','280010','280020','290010','290020','300010','300020','310010','310020','320010',
'320020','320030','330010','330020','340010','340020','350010','350020','350030','350040',
'360010','360020','370000','380010','380020','380030','390010','390020','390030','400010',
'400020','400030','400040','410010','410020','420010','420020','420030','420040','430010',
'430020','430030','430040','440010','440020','440030','440040','450010','450020','450030',
'450040','460010','460020','460030','460040','471010','471020','471030','472000','473000',
'474010','474020']
Tname=["稚内","旭川","留萌", "網走", "北見", "紋別", "根室", "釧路", "帯広", "室蘭", "浦河", "札幌", "岩見沢","倶知安",
"函館","江差","青森", "むつ", "八戸","盛岡", "宮古", "大船渡","仙台", "白石", "秋田", "横手", "山形", "米沢", "酒田", 
"新庄", "福島", "小名浜","若松", "水戸", "土浦", "宇都宮","大田原","前橋", "みなかみ","さいたま","熊谷", "秩父", "千葉", 
"銚子", "館山", "東京", "大島", "八丈島","父島", "横浜", "小田原","新潟", "長岡", "高田", "相川", "富山", "伏木", "金沢", 
"輪島", "福井", "敦賀", "甲府", "河口湖","長野", "松本", "飯田", "岐阜", "高山", "静岡", "網代", "三島", "浜松", "名古屋",
"豊橋", "津", "尾鷲", "大津", "彦根", "京都", "舞鶴", "大阪", "神戸", "豊岡", "奈良", "風屋", "和歌山","潮岬", "鳥取", 
"米子", "松江", "浜田", "西郷", "岡山", "津山", "広島", "庄原", "下関","山口", "柳井", "萩", "徳島", "日和佐","高松", 
"松山", "新居浜","宇和島","高知", "室戸岬","清水", "福岡", "八幡", "飯塚", "久留米","佐賀", "伊万里","長崎", "佐世保",
"厳原", "福江", "熊本", "阿蘇乙姫","牛深", "人吉", "大分", "中津", "日田", "佐伯", "宮崎", "延岡", "都城", "高千穂",
"鹿児島","鹿屋", "種子島","名瀬", "那覇", "名護", "久米島","南大東","宮古島","石垣島","与那国島"]

#対話内容まとめ
tellDay = "1か所の天気情報ですね。分かりました！\nでは次に、天気を知りたい日を、今日、明日、明後日の中から選んでください。"
tellDayError = "知りたい天気の形態を1か所or2か所で指定してください。\n＜ワンポイントアドバイス＞\n1か所は天気をピンポイントで調べるのに、2か所は旅行やお出かけなどお出かけ先の天気を調べるのに適しています！"
tellBasyo = "の天気情報ですね。分かりました！\nでは次に、知りたい場所の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく！)"
tellBasyoKwsk = "の天気情報ですね。分かりました！\nでは最後に、知りたい場所に最も近い場所を選んでください。"
checkBasyoKwsk = "の天気情報ですね。分かりました！\nそれでは、"
###################################################


#決まり文句
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



