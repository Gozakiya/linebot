# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests, strip, time, datetime


def train_trouble():
    #--------- get train route info---------
    ##input departure and destination station
    departure_station = "川崎" #DepartureStation　#出発駅

    destination_station = "自由が丘" #DestinationStation    #到着駅

    ##input time parameter of now
    today = datetime.datetime.fromtimestamp(time.time())
 

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


print(train_trouble())



# print(route_url)

print("finish")




#----------------------Trash Box--------------

# transfer_count = route_soup.find_all(class_ = "transfer") #乗り換え回数all
# for element in transfer_count:
#     print(element.text)

# trouble_route = route_soup.find_all(class_ = "transport") #路線all
# for element2 in trouble_route:
#     print(element2.text)

# #routes_a = route_soup.find("div",class_ = "mdSearchResult")
# route_number = route_soup.find(id = 'route01')
# #route_number = routes_all.find("div",id_ = "route01") 
# print(route_number.text)
# route_summary = route_number.find("dl",class_ = "routeSummary")            # 経路のサマリー
# print(route_summary)
# transfer_count = route_summary.find("li", class_ = "transfer").get_text() #乗り換え回数