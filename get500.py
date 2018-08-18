# Very inefficient way of retrieving the data of the top 500 coins every 5 minutes. 

import requests, json, csv, time, datetime, os, sys, urllib2, json, pymongo
from bson import json_util
from pymongo import MongoClient

url = "https://api.coinmarketcap.com/v1/ticker/?limit=500"
client = MongoClient('mongodb://%s:%s@localhost:27017/' % ('hyoonflask', 'IwIgi2BCCe!'))
db = client.lunarlabz
collection = db.top500

while True:
    resp = requests.get(url = url)
    obj = resp.json()
    top500list = []
    for coin in obj:
        data = {}
        data['_id'] = coin['symbol']
        data['fullname'] = coin['name']
        data['symbol'] = coin['symbol']
        data['rank'] = int(coin['rank'])
        try:
            data['market_cap_usd'] = float(coin['market_cap_usd'])
        except:
            data['market_cap_usd'] = float('0')
            pass
        data['price_usd'] = float(coin['price_usd'])
        data['price_btc'] = float(coin['price_btc'])
        data['last_updated'] = coin['last_updated']
        try:
            data['24h_volume_usd'] = float(coin['24h_volume_usd'])
        except:
            data['24h_volume_usd'] = float('0')
            pass
        try:
            data['percent_change_1h'] = float(coin['percent_change_1h'])
        except:
            data['percent_change_1h'] = float('0')
            pass
        try:
            data['percent_change_24h'] = float(coin['percent_change_24h'])
        except:
            data['percent_change_24h'] = float('0')
            pass
        try:
            data['percent_change_7d'] = float(coin['percent_change_7d'])
        except:
            data['percent_change_7d'] = float('0')
            pass
        top500list.append(data)




    obj_json = json.dumps({'listofCoins': top500list})
    data2 = json_util.loads(obj_json, encoding=None, cls=None,
        object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None,
        object_pairs_hook=None)
    top500 = collection.insert(data2)
    #print(type(data2))
    #print(data2)
    print("Next update in 5 minutes")
    time.sleep(300)
