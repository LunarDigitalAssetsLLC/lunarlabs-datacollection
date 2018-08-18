#!/usr/bin/env python
# -- coding: utf-8 --
import requests
import time
import pandas as pd
from tabulate import tabulate

mode = 'usd' #compare in usd or krw
interval = 30 #seconds between each check

#BFX USD
bitfinexSymbols = 'https://api.bitfinex.com/v1/symbols'
bitfinexLink = 'https://api.bitfinex.com/v2/tickers?symbols=' #tBTCUSD,tETHUSD
bitfinexCoins = ['BTC','LTC','ETH','ETC','RRT','ZEC','XMR','DSH','XRP','IOT','EOS','SAN','OMG','BCH','NEO','ETP','QTM','AVT',\
'EDO','BTG','DAT','QSH','YYW','GNT','SNT','SPK','TRX','RCN','RLC','AID','SNG','REP','ELF']
bitfinexPairs = ''
for coin in bitfinexCoins:
    bitfinexPairs += 't' + coin + 'USD,'
bitfinexPairs = bitfinexPairs[:-1]

bitfinexFixlist = { 'DSH':'DASH', 'QTM':'QTUM' , 'DAT':'DATA' , 'QSH':'QASH' , 'YYW':'YOYOW',\
'SPK':'SPANK', 'SNG':'SNGLS'}
#Fix tickers : DSH QTM DAT QSH YYW SPK SNG    -- Fix handled inside loop

hitbtcLink = 'https://api.hitbtc.com/api/2/public/ticker'
hitbtcPairs = '' #N/A filtered in code

bithumbLink = 'https://api.bithumb.com/public/ticker/ALL'
bithumbPairs = '' #N/A all bithumb pairs are KRW

upbitLink = 'https://crix-api-endpoint.upbit.com/v1/crix/recent?codes='
upbitPairs = ['ADA','ARDR','ARK','BCC','BTC','BTG','DASH','EMC2','ETC','ETH','GRS','KMD','LSK','LTC'\
,'MER','MTL','NEO','OMG','PIVX','POWR','QTUM','REP','SBD','SNT','STEEM','STORJ','STRAT','TIX','VTC'\
,'WAVES','XEM','XLM','XRP','ZEC']
upbitAllPairs = ''
for coin in upbitPairs:
    upbitAllPairs += 'CRIX.UPBIT.KRW-' + coin + ','
upbitAllPairs = upbitAllPairs[:-1]
upbitFixlist = { 'BCC':'BCH' }


header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
conversionRateLink = 'https://api.fixer.io/latest?base=USD'

while True:
    bitfinexPairPrices = {}
    hitbtcPairPrices = {}
    bithumbPairPrices = {}
    upbitPairPrices = {}

    print "Collecting Arbitrage Data from Bitfinex & HitBTC USD Pairs and Bithumb & Upbit KRW Pairs..."
    response = requests.get(conversionRateLink,headers=header).json()
    krwPerUSD = response['rates']['KRW']
    usdPerKRW = float(1) / float(krwPerUSD)

    #Handle bitfinex
    response = requests.get(bitfinexLink + bitfinexPairs,headers=header).json()
    for coin in response:
        coinFormatted = coin[0][1:-3]
        if coinFormatted in bitfinexFixlist:
            coinFormatted = bitfinexFixlist[coinFormatted]
        data = [coin[7],'Bitfinex']
        bitfinexPairPrices[coinFormatted] = data

    # print "BitfinexPairs"
    # print bitfinexPairPrices
    # print("\n")

    #Handle hitbtc
    response = requests.get(hitbtcLink,headers=header).json()
    for coin in response:
        if coin['symbol'][-3:] == 'USD':
            data = [coin['last'],'HitBTC']
            hitbtcPairPrices[coin['symbol'][:-3]] = data

    # print "HitbtcPairs"
    # print hitbtcPairPrices
    # print("\n")

    #Handle bithumb
    response = requests.get(bithumbLink,headers=header).json()
    obj = response['data']
    for coin, price in obj.items():
        if coin != 'date':
            data = [price['sell_price'],'Bithumb']
            bithumbPairPrices[coin] = data

    # print "BithumbPairs"
    # print bithumbPairPrices
    # print("\n")

    #Handle upbit
    response = requests.get(upbitLink+upbitAllPairs,headers=header)
    response = response.json()
    for item in response:
        coinFormatted = item['code'][15:]
        if coinFormatted in upbitFixlist:
            coinFormatted = upbitFixlist[coinFormatted]
        data = [item['tradePrice'],'Upbit']
        upbitPairPrices[coinFormatted] = data

    # print "UpbitPairs"
    # print upbitPairPrices
    # print("\n")

    #Compile a list of all USD Coins
    # print "Compiling USD Coin Master List..."
    usdCoinMap = bitfinexPairPrices
    for key, value in hitbtcPairPrices.items():
        if key in usdCoinMap: #compare
            if float(value[0]) < float(usdCoinMap[key][0]):
                #print key + " is cheaper on Hitbtc than Bitfinex"
                usdCoinMap[key] = value
        else:
            usdCoinMap[key] = value

    #Compile a list of all KRW Coins
    # print "Compiling KRW Coin Master List..."
    krwCoinMap = bithumbPairPrices
    for key, value in upbitPairPrices.items():
        if key in krwCoinMap: #compare
            if float(value[0]) < float(krwCoinMap[key][0]):
                #print key + " is cheaper on Upbit than Bithumb"
                krwCoinMap[key] = value
        else:
            krwCoinMap[key] = value

    # print"Trimming USD"
    deleteListUSD = []
    for key in usdCoinMap:
        if key not in krwCoinMap:
            deleteListUSD.append(key)

    for item in deleteListUSD:
        del usdCoinMap[item]

    # print"Trimming KRW"
    deleteListKRW = []
    for key in krwCoinMap:
        if key not in usdCoinMap:
            deleteListKRW.append(key)

    for item in deleteListKRW:
        del krwCoinMap[item]

    #if all in KRW
    if mode is 'krw':
        print "Mode: KRW\n"
        for key, value in usdCoinMap.items():
            value[0] = float(value[0]) * krwPerUSD

    elif mode is 'usd':
    #else all in USD
        print "Mode: USD\n"
        for key, value in krwCoinMap.items():
            value[0] = float(value[0]) * usdPerKRW

    df_cols = ['Coin','% Diff','Exchange A','Price A', 'Exchange B', 'Price B']

    dataList = []

    for key, value in usdCoinMap.items():
        valueUSD = round(float(value[0]),2)
        exchangeUSD = value[1]
        valueKRW = round(float(krwCoinMap[key][0]),2)
        exchangeKRW = krwCoinMap[key][1]
        difference = round(100 * (valueKRW - valueUSD) / valueUSD,2)
        if difference < 0:
            dataList.append([key, difference*-1, exchangeKRW, valueKRW, exchangeUSD, valueUSD])
            #print "{} is {}% cheaper on {} @ {}USD than {} @ {}USD!".format(key, difference*-1, exchangeKRW, valueKRW, exchangeUSD, valueUSD)
        else:
            dataList.append([key, difference, exchangeUSD, valueUSD, exchangeKRW, valueKRW])
            #print "{} is {}% cheaper on {} @ {}USD than {} @ {}USD!".format(key, difference, exchangeUSD, valueUSD, exchangeKRW, valueKRW)

    df = pd.DataFrame(dataList,columns=df_cols)
    pd.set_option('colheader_justify', 'right')
    df = df.sort_values(by='% Diff',ascending=False)
    print df.to_string(justify='center',index=False)

    print "\nNext check in {} seconds...\n".format(interval)
    time.sleep(interval)
