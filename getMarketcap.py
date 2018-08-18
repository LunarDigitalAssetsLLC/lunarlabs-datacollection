# Very primitive way of updating the global market cap every three minutes.

import requests, time, os, sys, urllib2, json, pymongo
from bson import json_util
from pymongo import MongoClient


url = "https://api.coinmarketcap.com/v1/global/"

client = MongoClient('mongodb://%s:%s@localhost:27017/' % ('hyoonflask', 'IwIgi2BCCe!'))

db = client.lunarlabz
collection = db.globalData

while True:
	resp = requests.get(url=url)
	obj = resp.json()
	#print(obj)
	marketData = collection.insert(obj)
	print("Next update in 3 minutes")
	time.sleep(180)
