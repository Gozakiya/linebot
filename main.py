import sys
sys.path.append("/home/user/Source/Machine_Learning_Project")

import config   # 先ほど作成したconfig.pyをインポート
from flask import Flask, request, abort

from bs4 import BeautifulSoup as bs
import requests, strip, time, datetime



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

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)    # config.pyで設定したチャネルアクセストークン
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)    # config.pyで設定したチャネルシークレット
 
#接続確認ルート
@app.route("/")
def root():
    return "Hello, Flask!"


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
 
    return 'OK'
 
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
 
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
##【以下にお出かけアプリのコードを記載】###

def train_trouble():
    #--------- get train route info---------
    ##input departure and destination station
    departure_station = "川崎" #DepartureStation　#出発駅

    destination_station = "自由が丘" #DestinationStation    #到着駅

    ##input time parameter of now
    today = datetime.datetime.fromtimestamp(time.time())
    #datetime.datetime(2019, 12, 2, 0, 7, 11, 120307)

    # print(today)

    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    hour = today.strftime("%H")
    minute = today.strftime("%M")
    m1 = minute[0]
    m2 = minute[1]

    # print(year)
    # print(m1)
    # print(m2)


    ##webページから情報を取得
    route_url="https://transit.yahoo.co.jp/search/result?from=" + departure_station +"&to=" + destination_station +"&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=" + year +"&m=" + month + "&d="+ day +"&hh=" + hour +"&m1=" + m1 + "&m2=" + m2 + "&type=1&ticket=ic&expkind=1&userpass=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1#route01"

    route_response = requests.get(route_url) #Requestsを利用してWebページを取得する
    route_soup = bs(route_response.text, 'html.parser') # BeautifulSoupを利用してWebページを解析する

    #------- get trouble info
    trouble_route = route_soup.find_all(class_ ="access trouble") #遅延all


    # 遅延の判定

    list_trouble = []
    if trouble_route == [] :
        result = "遅延なし"
    else:
        #print("遅延あり")
        for element2 in trouble_route:  
            dot= element2.text.find("線"or"ライン")#("・")
            start = len("[line][train]")
            element2 = element2.text[start:dot+1]
            list_trouble.append(element2)

        # print(list_trouble)
        list_trouble = set(list_trouble)
        result = "遅延が発生している路線は以下の通りです。"
        for i in list_trouble:
            #print("・" + i)
            result = result + "\n・" + i
    return result
   








#######################################

if __name__ == "__main__":
    # webサーバーの立ち上げ
    app.run(host='0.0.0.0')
