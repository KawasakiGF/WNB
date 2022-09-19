import re
import requests
import os
import json
import urllib.request
import random
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
          self.context = "0"
          self.date = 0
          self.area = ""
          self.areaT = ""
          self.basyoList = ""
          self.date2 = 0
          self.area2 = ""
          self.areaT2 = ""
          self.basyoList2 = ""
          self.count = 0

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


    def get_date2(self):
        return self.date2
    def set_date2(self, date2):
          self.date2 = date2

    def get_area2(self):
        return self.area2
    def set_area2(self, area2):
          self.area2 = area2

    def get_areaT2(self):
        return self.areaT2
    def set_areaT2(self, areaT2):
          self.areaT2 = areaT2

    def get_basyoList2(self):
        return self.basyoList2
    def set_basyoList2(self, basyoList2):
          self.basyoList2 = basyoList2

    def get_para(self):
        return self.para
    def set_para(self, para):
          self.para = para

    def get_count(self):
        return self.count
    def set_count(self, count):
          self.count = count



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


    def read_date2(user_id):
        return MySession._status_map.get(user_id).get_date2()
    def update_date2(user_id, date2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_date2(date2)
        MySession._status_map[user_id] = new_status

    def read_area2(user_id):
        return MySession._status_map.get(user_id).get_area2()
    def update_area2(user_id, area2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_area2(area2)
        MySession._status_map[user_id] = new_status

    def read_areaT2(user_id):
        return MySession._status_map.get(user_id).get_areaT2()
    def update_areaT2(user_id, areaT2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_areaT2(areaT2)
        MySession._status_map[user_id] = new_status

    def read_basyoList2(user_id):
        return MySession._status_map.get(user_id).get_basyoList2()
    def update_basyoList2(user_id, basyoList2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_basyoList2(basyoList2)
        MySession._status_map[user_id] = new_status

    def read_para(user_id):
        return MySession._status_map.get(user_id).get_para()
    def update_para(user_id, para):
        new_status = MySession._status_map.get(user_id)
        new_status.set_para(para)
        MySession._status_map[user_id] = new_status

    def read_count(user_id):
        return MySession._status_map.get(user_id).get_count()
    def update_count(user_id, count):
        new_status = MySession._status_map.get(user_id)
        new_status.set_count(count)
        MySession._status_map[user_id] = new_status



#都道府県コードを返す
def todoufukenNum(num):
     if num < 9:
          codeNum = num + 1
          return "0" + str(codeNum)
     elif num == 9:
          return "10"
     else:
          codeNum = num + 1
          return str(codeNum)

#都道府県の場所コード探す
def codeKaraFind(finder):
     teijiBasyoList = ""
     for i in range(0, len(Tcode)):
          if re.match((finder + "...."), Tcode[i]):
               teijiBasyoList += "\n・" + Tname[i]

     return teijiBasyoList
      
#天気メッセージを作る
def OtenkiMessageMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     date="--"
     weather="--"
     tempMAX=0
     tempMIN=0
     amCOR="--"
     pmCOR="--"
     date=jsonData["forecasts"][itu]["date"]
     weather=jsonData["forecasts"][itu]["telop"]
     tempMAX=jsonData["forecasts"][itu]["temperature"]["max"]["celsius"]
     tempMIN=jsonData["forecasts"][itu]["temperature"]["min"]["celsius"]
     amCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T06_12"]
     pmCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T12_18"] 
     #天気メッセージ作成
     tenkiInfo = '＜日付＞:{0}\n＜天気＞:{1}\n＜気温＞\n最低気温:{2}℃\n最高気温:{3}℃\n＜降水確率＞\n午前:{4}　午後{5}'.format(date,weather,tempMIN,tempMAX,amCOR,pmCOR)
     return tenkiInfo

#知りたい場所の天気を作る
def needWeatherMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     weather="--"
     weather=jsonData["forecasts"][itu]["telop"]
     return weather

#気温の平均を作る
def tempMEANMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     tempMAX=0
     tempMIN=0
     tempMAX=jsonData["forecasts"][itu]["temperature"]["max"]["celsius"]
     tempMIN=jsonData["forecasts"][itu]["temperature"]["min"]["celsius"]
     if ((tempMAX is None) and (tempMIN is None)):
        tempMAX == 100
        tempMIN == 100
     elif tempMAX is None: tempMAX=tempMIN
     elif tempMIN is None: tempMIN=tempMAX
     tempMEAN=(int(tempMAX)+int(tempMIN))/2.0-1.0
     return tempMEAN

#1か所の傘の有無判定
def kasaHantei(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     weather="--"
     amCOR="--"
     pmCOR="--"
     weather=jsonData["forecasts"][itu]["telop"]
     amCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T06_12"]
     pmCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T12_18"]
     AC=re.sub(r"\D", "", amCOR)
     PC=re.sub(r"\D", "", pmCOR)
     if ((AC == "") and (PC == "")):
        kasaInfo = "傘情報を取得できませんでした。"
        return kasaInfo
     elif AC == "": AC=PC
     elif PC == "": PC=AC
     CORMEAN=int((int(AC)+int(PC))/2.0)
     if CORMEAN >= 50:
        kasaInfo = "雨が降りそうです。傘を持っていきましょう。"
     elif (CORMEAN >= 30 and "雨" in weather):
        kasaInfo = "雨が降りそうです。傘を持っていきましょう。"
     elif CORMEAN >= 30:
        kasaInfo = "雨が降らないこともありそうです。折り畳み傘があれば十分そうです。"
     else:
        kasaInfo = "傘は必要ありません。"
     return kasaInfo

#1か所の服装判定
def fukusouHantei(tempMEAN, weather):
  if tempMEAN <= 5:
    fukusou = '＜今日の服装＞\n重ね着をし、もふもふのコートやダウンジャケットの着用をするほか、手袋やマフラー、暖かい靴下など、できる限り暖かい服装選びをしましょう。'
  elif tempMEAN <= 9:
    fukusou = '＜今日の服装＞\n重ね着をし、ダウンコートやジャケットを着用しましょう。風が強いときは手袋やマフラーがあると安心です。'
  elif tempMEAN <= 13:
    fukusou = '＜今日の服装＞\nジャケットやコートなど、風を通さない服装にしましょう。ヒートテックがあると安心です。'
  elif tempMEAN <= 16 and weather == "晴れ":
    fukusou = '＜今日の服装＞\nニットやセーターにするか、風が無ければ軽い羽織りものを着るとよいでしょう。'
  elif tempMEAN <= 16:
    fukusou = '＜今日の服装＞\nニットやセーターでOKですが、寒く感じるときはジャケットやコートを着てもよいでしょう。'
  elif tempMEAN <= 19:
    fukusou = '＜今日の服装＞\n薄手のジャケットやパーカーにし、重ね着をするとよいでしょう。'
  elif tempMEAN <= 22:
    fukusou = '＜今日の服装＞\n着脱可能な羽織りものにし、温度に合わせて調節できるようにしましょう。'
  elif tempMEAN <= 24:
    fukusou = '＜今日の服装＞\n長袖が一枚あればOKです。半袖と薄い羽織りものでもよいでしょう。'
  elif tempMEAN <= 29:
    fukusou = '＜今日の服装＞\n半袖で過ごせそうです。長袖にして腕まくりをするのもよいでしょう。'
  elif tempMEAN <= 99:
    fukusou = '＜今日の服装＞\n半袖の涼しい服装にし、暑さ対策や熱中症対策を怠らないようにしましょう。'
  else:
    fukusou = '＜今日の服装＞\n気温の情報を取得できませんでした。'
  return fukusou

#2か所の服装判定
def fukusouHantei2(STM, MTM, para):
  kandansa = ""
  tempMEAN = int((int(STM)+int(MTM))/2.0) + para
  if STM-MTM >= 6:
    kandansa = "\n出発地と目的地で寒暖差が大きい可能性があります。羽織ものなど、温度調節をできる服を持っていくと良さそうです。"
  if tempMEAN <= 5:
    fukusou = '＜今日の服装＞\n重ね着をし、もふもふのコートやダウンジャケットの着用をするほか、手袋やマフラー、暖かい靴下など、できる限り暖かい服装選びをしましょう。'
  elif tempMEAN <= 9:
    fukusou = '＜今日の服装＞\n重ね着をし、ダウンコートやジャケットを着用しましょう。風が強いときは手袋やマフラーがあると安心です。'
  elif tempMEAN <= 13:
    fukusou = '＜今日の服装＞\nジャケットやコートなど、風を通さない服装にしましょう。ヒートテックがあると安心です。'
  elif tempMEAN <= 16 and weather == "晴れ":
    fukusou = '＜今日の服装＞\nニットやセーターにするか、風が無ければ軽い羽織りものを着るとよいでしょう。'
  elif tempMEAN <= 16:
    fukusou = '＜今日の服装＞\nニットやセーターでOKですが、寒く感じるときはジャケットやコートを着てもよいでしょう。'
  elif tempMEAN <= 19:
    fukusou = '＜今日の服装＞\n薄手のジャケットやパーカーにし、重ね着をするとよいでしょう。'
  elif tempMEAN <= 22:
    fukusou = '＜今日の服装＞\n着脱可能な羽織りものにし、温度に合わせて調節できるようにしましょう。'
  elif tempMEAN <= 24:
    fukusou = '＜今日の服装＞\n長袖が一枚あればOKです。半袖と薄い羽織りものでもよいでしょう。'
  elif tempMEAN <= 29:
    fukusou = '＜今日の服装＞\n半袖で過ごせそうです。長袖にして腕まくりをするのもよいでしょう。'
  elif tempMEAN <= 99:
    fukusou = '＜今日の服装＞\n半袖の涼しい服装にし、暑さ対策や熱中症対策を怠らないようにしましょう。'
  else:
    fukusou = '＜今日の服装＞\n気温の情報を取得できませんでした。'
  return (fukusou + kandansa)

#2か所の傘の有無判定
def kasaHantei2(codeS, ituS, codeM, ituM, ST, MT):
     url="https://weather.tsukumijima.net/api/forecast/city/" + codeS
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     weather="--"
     amCOR="--"
     pmCOR="--"
     weather=jsonData["forecasts"][ituS]["telop"]
     amCOR=jsonData["forecasts"][ituS]["chanceOfRain"]["T06_12"]
     pmCOR=jsonData["forecasts"][ituS]["chanceOfRain"]["T12_18"]
     AC=re.sub(r"\D", "", amCOR)
     PC=re.sub(r"\D", "", pmCOR)
     if ((AC == "") and (PC == "")):
        kasaInfo = "傘情報を取得できませんでした。"
     elif AC == "": AC=PC
     elif PC == "": PC=AC
     CORMEANS=(int(AC)+int(PC))/2.0

     urlM="https://weather.tsukumijima.net/api/forecast/city/" + codeM
     responseM=requests.get(urlM)
     jsonDataM=responseM.json()
     #天気データ取得
     weatherM="--"
     amCORM="--"
     pmCORM="--"
     weatherM=jsonDataM["forecasts"][ituM]["telop"]
     amCORM=jsonDataM["forecasts"][ituM]["chanceOfRain"]["T06_12"]
     pmCORM=jsonDataM["forecasts"][ituM]["chanceOfRain"]["T12_18"]
     ACM=re.sub(r"\D", "", amCORM)
     PCM=re.sub(r"\D", "", pmCORM)
     if ((ACM == "") and (PCM == "")):
        kasaInfo2 = "傘情報を取得できませんでした。"
     elif ACM == "": ACM=PCM
     elif PCM == "": PCM=ACM
     CORMEANM=(int(ACM)+int(PCM))/2.0

     CORMEAN = int((CORMEANS+CORMEANS)/2.0)

     if CORMEANS >= 50 and CORMEANM >= 50:
        kasaInfo = "雨が降りそうです。傘を持っていきましょう。"
     elif (CORMEANS >= 50 and (CORMEANM >= 30 and "雨" in weather)) or (CORMEANM >= 50 and (CORMEANS >= 30 and "雨" in weather)):
        kasaInfo = "雨が降りそうです。傘を持っていきましょう。"
     elif (CORMEANS >= 50 or (CORMEANS >= 30 and "雨" in weather)) and CORMEANM < 30:
        kasaInfo = ST + "では雨が降りそうですが、" + MT + "では雨が降らなさそうです。傘を持つ余裕があれば傘を、無ければ折り畳み傘を持っていきましょう。"
     elif (CORMEANM >= 50 or (CORMEANM >= 30 and "雨" in weather)) and CORMEANS < 30:
        kasaInfo = ST + "では雨が降らなさそうですが、" + MT + "では雨が降りそうです。傘を持つ余裕があれば傘を、無ければ折り畳み傘を持っていきましょう。"
     elif CORMEANS >= 30 or CORMEANM >= 30:
        kasaInfo = "雨が降らないこともありそうです。折り畳み傘があれば十分でしょう。"
     else:
        kasaInfo = "傘は必要ありません。"
     return kasaInfo

#天気アイコン判定
def picUrlMaker(weather):
    if weather=="晴れ" or weather=="晴山沿い雷雨" or weather=="晴山沿い雪" or weather=="朝の内霧後晴" or weather=="晴明け方霧":
        picUrl="https://i.ibb.co/v3Q1SzX/Sun.png"
    elif weather=="晴のち曇" or weather=="晴のち一時曇" or weather=="晴のち時々曇":
        picUrl="https://i.ibb.co/47Zp7tf/Sun-To-Cloud.png"
    elif weather=="晴のち雨" or weather=="晴のち一時雨" or weather=="晴のち時々雨" or weather=="晴のち雨か雪" or weather=="晴のち雨か雷雨" or weather=="晴夕方一時雨" or weather=="晴午後は雷雨" or weather=="晴昼頃から雨" or weather=="晴夕方から雨" or weather=="晴夜は雨" or weather=="晴夜半から雨":
        picUrl="https://i.ibb.co/w6yBmKP/Sun-To-Rain.png"
    elif weather=="晴のち雪" or weather=="晴のち一時雪" or weather=="晴のち時々雪" or weather=="晴のち雪か雨":
        picUrl="https://i.ibb.co/2hWsVQy/Sun-To-Snow.png"
    #存在しないパターン
    elif weather=="晴時々曇" or weather=="晴一時曇":
        picUrl="https://i.ibb.co/vJn5mwZ/Sun-Or-Cloud.png"
    elif weather=="晴時々雨" or weather=="晴一時雨" or weather=="晴時々雨か雪" or weather=="晴一時雨か雪" or weather=="晴一時雨か雷雨" or weather=="晴朝夕一時雨" or weather=="晴時々雨で雷雨を伴う":
        picUrl="https://i.ibb.co/cc9c8F1/Sun-Or-Rain.png"
    elif weather=="晴時々雪" or weather=="晴一時雪" or weather=="晴時々雪か雨" or weather=="晴一時雪か雨":
        picUrl="https://i.ibb.co/gZvsSzn/Sun-Or-Snow.png"
    elif weather=="曇り" or weather=="霧" or weather=="曇海上海岸は霧か霧雨":
        picUrl="https://i.ibb.co/V32pwjv/Cloud.png"
    elif weather=="曇のち晴" or weather=="曇のち一時晴" or weather=="曇のち時々晴":
        picUrl="https://i.ibb.co/wwc1J9P/Cloud-To-Sun.png"
    elif weather=="曇のち雨" or weather=="曇のち一時雨" or weather=="曇のち時々雨" or weather=="曇のち雨か雪" or weather=="曇のち雨か雷雨" or weather=="曇夕方一時雨" or weather=="曇昼頃から雨" or weather=="曇夕方から雨" or weather=="曇夜は雨" or weather=="曇夜半から雨":
        picUrl="https://i.ibb.co/mSXWrsm/Cloud-To-Rain.png"
    elif weather=="曇のち雪" or weather=="曇のち一時雪" or weather=="曇のち時々雪" or weather=="曇昼頃から雪" or weather=="曇夕方から雪" or weather=="曇夜は雪" or weather=="曇のち雪か雨":
        picUrl="https://i.ibb.co/Tv42FLY/Cloud-To-Snow.png"
    elif weather=="曇時々晴" or weather=="曇一時晴" or weather=="曇日中時々晴":
        picUrl="https://i.ibb.co/XX9sp2Y/Cloud-Or-Sun.png"
    elif weather=="曇時々雨" or weather=="曇一時雨" or weather=="曇時々雨か雪" or weather=="曇一時雨か雪" or weather=="曇一時雨か雷雨" or weather=="曇朝方一時雨" or weather=="曇時々雨で雷を伴う":
        picUrl="https://i.ibb.co/fkRCR7m/Cloud-Or-Rain.png"
    elif weather=="曇時々雪" or weather=="曇一時雪" or weather=="曇時々雪で雷を伴う" or weather=="曇一時雪か雨" or weather=="曇時々雪か雨":
        picUrl="https://i.ibb.co/9nyfKy5/Cloud-Or-Snow.png"
    elif weather=="雨" or weather=="大雨" or weather=="風雨共に強い" or weather=="雨一時強く降る" or weather=="雨で雷を伴う":
        picUrl="https://i.ibb.co/5xkdS8V/Rain.png"
    #存在しないパターン
    elif weather=="雨のち曇" or weather=="雨のち一時曇" or weather=="雨のち時々曇" or weather=="雨か雪のち曇" or weather=="朝の内雨のち曇":
        picUrl="https://i.ibb.co/vPgg2nt/Rain-To-Cloud.png"
    elif weather=="雨のち晴" or weather=="晴朝の内一時雨" or weather=="雨か雪のち晴" or weather=="朝の内雨のち晴" or weather=="雨昼頃から晴" or weather=="雨夕方から晴" or weather=="雨夜は晴":
        picUrl="https://i.ibb.co/mzYX8j4/Rain-To-Sun.png"
    elif weather=="雨のち雪" or weather=="雨のち一時雪" or weather=="雨のち時々雪" or weather=="雨夕方から雪" or weather=="雨夜は雪":
        picUrl="https://i.ibb.co/GsMs2bN/Rain-To-Snow.png"
    elif weather=="雨時々曇" or weather=="雨一時曇" or weather=="雨時々止む" or weather=="雨一時止む":
        picUrl="https://i.ibb.co/TbR1wRW/Rain-Or-Cloud.png"
    elif weather=="雨時々晴" or weather=="雨一時晴":
        picUrl="https://i.ibb.co/9sdjnNs/Rain-Or-Sun.png"
    elif weather=="雨時々雪" or weather=="雨一時雪" or weather=="雨か雪" or weather=="雨朝晩一時雪" or weather=="雨一時霙" or weather=="雨一時みぞれ":
        picUrl="https://i.ibb.co/nMDzd7d/Rain-Or-Snow.png"
    elif weather=="雪" or weather=="雪一時強く降る":
        picUrl="https://i.ibb.co/qrDSG2F/Snow.png"
    elif weather=="雪のち曇" or weather=="雪か雨のち曇" or weather=="朝の内雪のち曇":
        picUrl="https://i.ibb.co/qdftDWR/Snow-To-Cloud.png"
    elif weather=="雪のち晴" or weather=="雪か雨のち晴" or weather=="朝の内雪のち晴":
        picUrl="https://i.ibb.co/d4y70W9/Snow-To-Sun.png"
    elif weather=="雪のち雨" or weather=="雪のち霙" or weather=="雪のちみぞれ" or weather=="雪昼頃から雨" or weather=="雪夕方から雨" or weather=="雪夜から雨" or weather=="雪夜半から雨":
        picUrl="https://i.ibb.co/KqnPzr7/Snow-To-Rain.png"
    elif weather=="雪時々曇" or weather=="雪一時曇" or weather=="雪時々止む" or weather=="雪一時止む":
        picUrl="https://i.ibb.co/ZmYkPZW/Snow-Or-Cloud.png"
    elif weather=="雪時々晴" or weather=="雪一時晴":
        picUrl="https://i.ibb.co/y8M4vgH/Snow-Or-Sun.png"
    elif weather=="雪時々雨" or weather=="雪一時雨" or weather=="雪か雨" or weather=="雪一時霙" or weather=="雪一時みぞれ":
        picUrl="https://i.ibb.co/Zm5JnKh/Snow-Or-Rain.png"
    elif weather=="暴風雨" or weather=="雨で暴風を伴う":
        picUrl="https://i.ibb.co/y6X5z5X/Typhon.png "
    elif weather=="暴風雪" or weather=="大雪" or weather=="風雪強い" or weather=="雪で雷を伴う":
        picUrl="https://i.ibb.co/2NMQLDS/Heavy-Snow.png"
    else: picUrl="未知の天気"
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

##############################################
##########実行するプログラムの内容をここに書く################
#@handler.addのメソッドの引数にはイベントのモデルを入れる(MessageEvent=メッセージを受けたら)
@handler.add(MessageEvent,message=TextMessage)
#関数名handle_messageは自由
#statusで1か所or2か所を管理。1x...1か所。2x...2か所
def handle_message(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    talk = event.message.text

    MySession.register(user_id)

#会話を中断したいとき
    if (talk == "リセット"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("最初からリセットします。1か所or2か所を入力してください。"))
        # 現在のstatusを消して新規statusで初期化。
        MySession.reset(user_id)

#いつものセットでお天気検索
    if MySession.read_context(user_id) == "0" and (talk == "いつもの" or talk == "いつもので" or talk == "いつものでお願い" or talk == "いつものでおねがい"):
          para = MySession.read_para(user_id)
          picUrl = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          fukusouInfo = fukusouHantei((tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)) + int(para)), needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          tenkiInfo = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          kasaInfo = kasaHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          if picUrl == "未知の天気":
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！"),
                    TextSendMessage(text=tenkiInfo),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo)])
          else:
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！"),
                    TextSendMessage(text=tenkiInfo),
                    ImageSendMessage(original_content_url=picUrl, preview_image_url=picUrl),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo)])

#1か所の場所を聞く####################
    if MySession.read_context(user_id) == "0" and ("1" in talk or "１" in talk or "一" in talk):
       if "1" in talk or "１" in talk or "一" in talk:
          MySession.reset(user_id)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDay))
          MySession.update_context(user_id, "10")
          MySession.update_count(user_id, 0)
       else:
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDayError))

#日にちを聞く
    elif MySession.read_context(user_id) == "10":
       if ("今日" in talk or "きょう" in talk) or ("明日" in talk or "あした" in talk) or ("明後日" in talk or "あさって" in talk):
           if "今日" in talk or "きょう" in talk:    MySession.update_date(user_id, 0)
           elif "明日" in talk or "あした" in talk: MySession.update_date(user_id, 1)
           else:                                                       MySession.update_date(user_id, 2)
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
               TextSendMessage(text=(talk + tellBasyoKwsk + MySession.read_basyoList(user_id))))
          MySession.update_context(user_id, "12")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="知りたい場所" + tellBasyoError))


#1か所の場所の詳細を聞く
    elif MySession.read_context(user_id) == "12":
       if talk in MySession.read_basyoList(user_id):
          MySession.update_area(user_id, talk)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=("知りたい場所は" + MySession.read_areaT(user_id) + talk + tellHotOrCold)))
          MySession.update_context(user_id, "13")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= tellBasyoKwskError +  MySession.read_basyoList(user_id)))

#体調を聞く&1か所の天気情報を教える
    elif MySession.read_context(user_id) == "13":
       if "暑" in talk or "あつ" in talk or "寒" in talk or "さむ" in talk or "どちら" in talk or "どっち" in talk or "該当" in talk:
          if "暑" in talk or "あつ" in talk:
              MySession.update_para(user_id, 3)
              para = 3
          elif "寒" in talk or "さむ" in talk:
              MySession.update_para(user_id, -3)
              para = -3
          elif "どちら" in talk or "どっち" in talk or "該当" in talk:
              MySession.update_para(user_id, 0)
              para = 0
          picUrl = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          fukusouInfo = fukusouHantei((tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)) + int(para)), needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          tenkiInfo = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          kasaInfo = kasaHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          if picUrl == "未知の天気":
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！"),
                    TextSendMessage(text=tenkiInfo),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo + "\n∇次へ∇(任意文字を入力)")])
          else:
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！"),
                    TextSendMessage(text=tenkiInfo),
                    ImageSendMessage(original_content_url=picUrl, preview_image_url=picUrl),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo + "\n\n∇次へ∇(任意文字を入力)")])
          MySession.update_context(user_id, "14")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=tellHotOrColdError))

#１か所の情報保持を聞く
    elif MySession.read_context(user_id) == "14":
          if MySession.read_date(user_id) == 0: date="今日"
          elif MySession.read_date(user_id) == 1: date="明日"
          elif MySession.read_date(user_id) == 2: date="明後日"
          if MySession.read_para(user_id) == 3: para="暑がり"
          elif MySession.read_para(user_id) == 0: para="どちらでもない"
          elif MySession.read_para(user_id) == -3: para="寒がり"
          line_bot_api.reply_message(
             event.reply_token,
             [TextSendMessage(text="情報を保持しますか？保持する場合は「はい」を入力してください。\n保持すると、次回以降「いつもの」と入力すれば以下の条件で天気情報を検索できます！"),
             TextSendMessage(text="<日付>" + date + "\n<場所>" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n<体調>" + para)])
          MySession.update_context(user_id, "15")

#１か所の情報保持判定
    elif MySession.read_context(user_id) == "15":
       if talk == "はい" or talk == "保持する" or talk == "保持" or talk == "お願いします" or talk == "おねがいします" or talk == "おねがい" or talk == "お願い":
          if MySession.read_date(user_id) == 0: date="今日"
          elif MySession.read_date(user_id) == 1: date="明日"
          elif MySession.read_date(user_id) == 2: date="明後日"
          if MySession.read_para(user_id) == 3: para="暑がり"
          elif MySession.read_para(user_id) == 0: para="どちらでもない"
          elif MySession.read_para(user_id) == -3: para="寒がり"
          line_bot_api.reply_message(
             event.reply_token,
             [TextSendMessage(text="情報保持しました！次回以降「いつもの」と入力すれば以下の条件で天気情報を検索できます！"),
             TextSendMessage(text="<日付>" + date + "\n<場所>" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n<体調>" + para),
             TextSendMessage(text="情報は次の1か所or2か所の天気情報検索時まで保持されます。")])
          MySession.update_context(user_id, "0")
       else:
          line_bot_api.reply_message(
             event.reply_token,
             TextSendMessage(text="保持しませんでした。またご利用になられる場合は「1か所」もしくは「2か所」を入力してください"))
          MySession.reset(user_id)
###############################

#2か所の場所を聞く####################
    elif MySession.read_context(user_id) == "0" and ("2" in talk or "２" in talk or "二" in talk):
       if "2" in talk or "２" in talk or "二" in talk:
          MySession.reset(user_id)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDay2_1))
          MySession.update_context(user_id, "20")
          MySession.update_count(user_id, 0)
       else:
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDayError))

#出発する日にちを聞く
    elif MySession.read_context(user_id) == "20":
       if ("今日" in talk or "きょう" in talk) or ("明日" in talk or "あした" in talk) or ("明後日" in talk or "あさって" in talk):
           if "今日" in talk or "きょう" in talk:    MySession.update_date(user_id, 0)
           elif "明日" in talk or "あした" in talk: MySession.update_date(user_id, 1)
           else:                                                       MySession.update_date(user_id, 2)
           line_bot_api.reply_message(
           event.reply_token,
           TextSendMessage(text=tellBasyo2_1))
           MySession.update_context(user_id, "21")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「今日」、「明日」、「明後日」の中から入力してください。"))

#出発地の場所を聞く
    elif MySession.read_context(user_id) == "21":
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
               TextSendMessage(text=(talk + tellBasyoKwsk2_1 + MySession.read_basyoList(user_id))))
          MySession.update_context(user_id, "22")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="出発地" + tellBasyoError))

#出発地の場所の詳細を聞く
    elif MySession.read_context(user_id) == "22":
       if talk in MySession.read_basyoList(user_id):
          MySession.update_area(user_id, talk)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=("出発地は" + MySession.read_areaT(user_id) + talk + tellDay2_2)))
          MySession.update_context(user_id, "23")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= tellBasyoKwskError +  MySession.read_basyoList(user_id)))


#目的地に到着する日にちを聞く
    elif MySession.read_context(user_id) == "23":
       if ("今日" in talk or "きょう" in talk) or ("明日" in talk or "あした" in talk) or ("明後日" in talk or "あさって" in talk):
           if "今日" in talk or "きょう" in talk:    MySession.update_date2(user_id, 0)
           elif "明日" in talk or "あした" in talk: MySession.update_date2(user_id, 1)
           else:                                                       MySession.update_date2(user_id, 2)
           line_bot_api.reply_message(
           event.reply_token,
           TextSendMessage(text=tellBasyo2_2))
           MySession.update_context(user_id, "24")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「今日」、「明日」、「明後日」の中から入力してください。"))

#目的地の場所を聞く
    elif MySession.read_context(user_id) == "24":
       if talk in todoufuken:
          MySession.update_areaT2(user_id, talk)
          TBasyo2 = todoufukenNum(int(todoufuken.index(talk)))
          #TBasyoは文字型
          MySession.update_area2(user_id, TBasyo2)
          #area, basyoListは文字型
          kwsiBasyoList2 = codeKaraFind(MySession.read_area2(user_id))
          MySession.update_basyoList2(user_id, kwsiBasyoList2)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=(talk + tellBasyoKwsk2_2 + MySession.read_basyoList2(user_id))))
          MySession.update_context(user_id, "25")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="目的地" + tellBasyoError))

#目的地の場所の詳細を聞く
    elif MySession.read_context(user_id) == "25":
       if talk in MySession.read_basyoList2(user_id):
          MySession.update_area2(user_id, talk)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=("目的地は" + MySession.read_areaT2(user_id) + talk + tellHotOrCold)))
          MySession.update_context(user_id, "26")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= tellBasyoKwskError +  MySession.read_basyoList2(user_id)))

#体調を聞く&2か所の天気情報と総合情報を教える
    elif MySession.read_context(user_id) == "26":
       if "暑" in talk or "あつ" in talk or "寒" in talk or "さむ" in talk or "どちら" in talk or "どっち" in talk or "該当" in talk:
          if "暑" in talk or "あつ" in talk:
              MySession.update_para(user_id, 4)
              para = 4
          elif "寒" in talk or "さむ" in talk:
              MySession.update_para(user_id, -2)
              para = -2
          elif "どちら" in talk or "どっち" in talk or "該当" in talk:
              MySession.update_para(user_id, 1)
              para = 1
          picUrlS = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          tenkiInfoS = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          picUrlM = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date2(user_id)))
          tenkiInfoM = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date2(user_id))
          STM = tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          MTM = tempMEANMaker(Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date(user_id))
          fukusouInfo = fukusouHantei2(STM, MTM, para)
          ST = MySession.read_areaT(user_id) + MySession.read_area(user_id)
          MT = MySession.read_areaT2(user_id) + MySession.read_area2(user_id)
          kasaInfo = kasaHantei2(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id), Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date2(user_id), ST, MT)
          if picUrlS == "未知の天気" or picUrlM == "未知の天気":
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=MySession.read_areaT(user_id) + MySession.read_area(user_id) + "から" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "への天気情報を表示します！"),
                    TextSendMessage(text="[出発地]" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n" + tenkiInfoS),
                    TextSendMessage(text="[目的地]" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "\n" + tenkiInfoM),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo)])
          else:
               line_bot_api.reply_message(
                    event.reply_token,
                    #メッセージは1～5個まで
                    [#TextSendMessage(text=MySession.read_areaT(user_id) + MySession.read_area(user_id) + "から" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "への天気情報を表示します！"),
                    TextSendMessage(text="[出発地]" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n" + tenkiInfoS),
                    ImageSendMessage(original_content_url=picUrlS, preview_image_url=picUrlS),
                    TextSendMessage(text="[目的地]" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "\n" + tenkiInfoM),
                    ImageSendMessage(original_content_url=picUrlM, preview_image_url=picUrlM),
                    TextSendMessage(text=kasaInfo + "\n\n" +fukusouInfo)])
          MySession.reset(user_id)
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=tellHotOrColdError))

###############################

#その他の会話#######################
#'''
    elif MySession.read_context(user_id) == "0" and talk == "自己紹介してくれる？":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = jikosyoukai))
    elif MySession.read_context(user_id) == "0" and talk == "その帽子って？":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = bousiInfo))
    elif MySession.read_context(user_id) == "0" and talk == "制作秘話":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = seisakuhiwa))
    elif MySession.read_context(user_id) == "0" and talk == "雑談しよう":
        x = random.randint(0, len(zatudan)) - 1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = zatudan[x]))
    elif MySession.read_context(user_id) == "0" and ("こんぺいとう" in talk and "あげる" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = getKonpeitou))
    elif MySession.read_context(user_id) == "0" and (talk == "かわいい" or talk == "かわいいね" or talk == "教えてくれてありがとう" or talk == "お仕事ご苦労様" or talk == "お仕事えらいね" or talk == "お仕事偉いね" or talk == "お仕事がんばってるね" or talk == "お仕事がんばってね"):
        thanks = ""
        if talk == "教えてくれてありがとう": thanks = "こちらこそ、ご利用くださり誠に"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = thanks + "ありがとうございます！" + user_name +"さんのお役に立てるよう、精一杯頑張ります！"))
#'''
###############################

#該当しないメッセージが送られてきた場合#########
    else:
      MySession.update_count(user_id, worngCount+1)


###'''で囲めばその間の行をコメントアウトできる
###以下は間違えすぎた時のBOTの反応######
#'''
      if MySession.read_count(user_id) >= 17:
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text=kaiwa1_4))
      elif MySession.read_count(user_id) == 16:
          rep = ""
          if rep == "うん" or rep == "せやで" or rep == "そうだよ" or rep == "そうだけど" or rep == "ばれた？":
              rep = talk + "、って...からかわないでくださいよもう。\n...あれ、"
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text=rep + kaiwa1_3))
      elif MySession.read_count(user_id) == 15:
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text=kaiwa1_2))
      elif MySession.read_count(user_id) > 10:
          line_bot_api.reply_message(
              event.reply_token,
              [TextSendMessage(text=kaiwa1_1),
              TextSendMessage(text=kaiwa1_1a)])
      else:
#'''
############################
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text="最初からやり直します。「1か所」or「2か所」を入力してください。"))
          #リプライはLineBotApiのメソッドを用いる。 第一引数のevent.reply_tokenはイベントの応答に
          #用いるトークン。 第二引数にはlinebot.modelsに定義されている返信用の
          #TextSendMessageオブジェクトを渡しています。

##################################
##############################################
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

#hotList = ["暑がり","あつがり","暑いのは苦手"]
#coldList = ["寒がり","さむがり","寒いのは苦手"]
#usualList = ["どちらでもない","どっちでもない","該当なし"]

#対話内容まとめ
tellDay = "1か所の天気情報ですね。分かりました！\nでは次に、いつの天気を知りたいか教えてください。ご提供できるのは「今日」、「明日」、「明後日」の3日です。"
tellDayError = "知りたい天気の場所を「1か所」or「2か所」で指定してください。\n＜ワンポイントアドバイス＞\n1か所は天気をピンポイントで調べるのに、2か所は旅行やお出かけなどお出かけ先の天気を調べるのに適しています！"
tellBasyo = "の天気情報ですね。分かりました！\nでは次に、知りたい場所の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく!)"
tellBasyoKwsk = "の天気情報ですね。分かりました！\nでは最後に、知りたい場所に最も近い場所を選んでください。"
tellHotOrCold = "ですね。分かりました!\n服装のおすすめをするにあたり、暑がりか、寒がりかについてお伺いしたいと思います。あなたは「暑がり」or「寒がり」のどちらに当てはまりますか？どちらでもない場合、「どちらでもない」と入力してください。"
tellHotOrColdError = "「暑がり」、「寒がり」、「どちらでもない」の中から入力してください。服装のおすすめ提示に使用させていただきます。"

tellDay2_1 = "2か所の天気情報ですね。分かりました!\nでは、始めに出発する日を教えてください。選択できるのは「今日」、「明日」、「明後日」の3日です。"
tellBasyo2_1 = "次に、出発地の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく！)"
tellBasyoError = "の都道府県を入力してください。\n入力したはずなのに、と思う場合は県、府、都、道が入力されていない可能性があります。"
tellBasyoKwsk2_1 = "の天気情報ですね。分かりました！\nでは次に、出発地に最も近い場所を選んでください。"
tellBasyoKwskError = "詳細な場所が選択できていないようです。以下に選択できるリストをもう一度表示しますので、この中からお選びください。"
tellDay2_2 = "ですね、承知しました!\nでは次に、目的地に到着する日の予定を教えてください。選択できるのは「今日」、「明日」、「明後日」の3日です。"
tellBasyo2_2 = "次に、目的地の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく!)"
tellBasyoKwsk2_2 = "の天気情報ですね。分かりました！\nでは次に、目的地に最も近い場所を選んでください。"

kaiwa1_1 = "あれれ、入力できてないです？「1か所」か「2か所」って入力してもらえば大丈夫ですよ。\n\nちゃんと入力してるのに、と思われた方へ。\nもしかしたらシステムエラーかもしれないので、日を改めてご利用いただきますようお願いいたします。"
kaiwa1_1a = "\n...実は、キーワードが「1(半角)」「１(全角)」「一(漢数字)」(2か所も同じ)って設定されてるので、例えば1って入力するだけでも通っちゃいます。入力ができていないようだったので、一度それで試してみていただけますか？"
kaiwa1_2 = "ちょっとちょっと、間違えすぎですって！\n...もしかして、わざと間違えてます？"
kaiwa1_3 = "ひょっとしてボクに話しかけてくれてますか？\n残念ながら、あなたとお話をしたくても、ボクはプログラムされた存在だからお話はできないんです。ごめんなさい..."
kaiwa1_4 = "ただ、ちょっとだけならお話できます。判定は厳しめなので、一文字でも間違えちゃダメですよ？\nこんなキーワードを入力してみてください。\n・「自己紹介してくれる？」\n・「その帽子って？」\n・「雑談しよう」"

jikosyoukai = "えっ、自己紹介ですか？分かりました！\nボクはフォグ。このぼっと？を取り仕切るお仕事をしてます！こんぺいとうと誰かのお役にたつことが好きです！まだまだ未熟者で至らない点がたくさんあるかもしれませんが、どうぞよろしくお願いいたします！"
bousiInfo = "これですか？これはボクのパパから譲り受けた帽子なんです。ボクの一族は代々この仕事に従事していて、ボクも最近着任したばかりなんですよ。"
seisakuhiwa = "卒研でのシステム開発をするにあたって、マスコットキャラクターを使うか否かを悩みましたね。ただ、対話型のBOTである以上会話してる感が欲しいし、有料無料問わず企業がこういったシステムを開発する際はキャラを用意することもあるだろうと思い使いました。\nただ、誰でも開発できるという部分には沿わないかもしれませんが..."
getKonpeitou = "えっいいんですか！？では遠慮なくいただ...あっ。\nそうだった、ここからじゃ受け取れませんよね...\nうう、お気持ちだけ頂戴いたします。ありがとうございます..."
zatudan = ["システムの仕様上、BOTからの返信が遅くなったり、返信が来なかったりすることがあります。それが顕著にみられるのが、「使い始め」と「暑がり寒がりを聞いた後」です。前者はBOTサーバーを起動するため、後者は情報取得と処理に時間がかかるから、反応が遅くなっちゃうんです。",
"「こんぺいとう」っておいしいですよね。あのポリポリっとした触感に、口に入れた瞬間に広がる優しい甘さ...。あれがたまらなく好きです。"]

###################################################


#決まり文句
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


