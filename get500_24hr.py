# Multithreaded ghetto way of updating the sparklines graph (column 4 of lunar labs homepage) every three minutes

import urllib2, json
from threading import Thread
from time import sleep
import numpy, math
import time, requests, csv, datetime, os, sys, urllib2, json, pymongo
from bson import json_util
import operator
from pymongo import MongoClient

client = MongoClient('mongodb://%s:%s@localhost:27017/' % ('hyoonflask', 'IwIgi2BCCe!'))
db = client.lunarlabz
collection = db.sparklinesData

print '[+] Getting fresh coin list from coincap'

req = urllib2.build_opener()
req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)')]
coinList = []
try:
    response = req.open(
        'http://coincap.io/map', timeout=20)
    data = json.load(response)
    for coin in data:
        coinList.append(coin['symbol'])
	list_to_remove = ['XDG','CLUB','SPK','AIO','JPY','IOS','RRT','SNG','BFT','SHND','CAD','GBG','ODE','GBP','YYW','NBT','STR','QSH','DSH','MNA','QTM','NANOX','USD','EUR','NEC']
	coinList= list(set(coinList).difference(set(list_to_remove)))
	coinList.extend(('SPANK','AION','YOYOW','USNBT','QASH','DASH','MANA','QTUM','NANO','IOT'))


except Exception, e:
    print '[!] Request for Coin List failed:.\n', e




#throw these in a config.json someday
threads = 30 #How many threads to run (Dont put this too high if your comp is a toaster)
intervalSeconds = 180 #How long between each check in seconds



def fetchPrices(name):
	req = urllib2.build_opener()
	req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)')]

	response = req.open('http://coincap.io/history/1day/' + str(name) + '/')
	data = json.load(response)
	prices = data['price']
	priceList = []
	for x in prices:
		priceList.append(x[1])
	return priceList[::3]

def insertData(name, pricelist):
	try:
		if (name == 'IOT'):
			name = 'MIOTA'
		addData = collection.update_one({'_id': name}, {"$set": { 'priceData': pricelist, 'lastUpdated': int(time.time()) }}, upsert = True)
	except Exception, e:
		print str(e)
		pass



def getBatch(thread, coins):
	while True:
		print("Running thread #{}".format(thread))
		for coin in coins:
			try:
				# print("Trying: " + str(coin))
				priceData = fetchPrices(coin)
				insertData(coin, priceData)
				#print(type(coin))
			except Exception as e:
				print("Exception Caught: " + coin)
				continue
				print "Exception: " + coin
		print("Thread # {} batch completed! Sleeping for 5min before repeating...".format(thread))
		sleep(intervalSeconds)


#IDC ERROR HANDLE
if __name__ == '__main__':
	try:
		os.makedirs(datapath)
	except OSError:
		if not os.path.isdir(datapath):
			raise

	#find how many coins to give each thread
	partitions = int(math.ceil( float(len(coinList)) / float(threads)))
	splitList = [coinList[i:i+partitions] for i in range(0,len(coinList),partitions)]

	#only need up to 1:1 thread:job
	if threads > coinList:
		threads = len(coinList)

	try:
		for x in range(0,threads):
			thread = Thread(target=getBatch,args=(x,splitList[x],))
			thread.daemon = True
			thread.start()
		while True:
			sleep(1)
	except KeyboardInterrupt:
		print("Exiting...")
		os._exit(0)
	except Exception as e:
		print("Global Exception: " + str(e))
		os._exit(0)
