import json
import time
import os
import math
import urllib.request
import requests

with open('list.txt') as rd:
    items = [x.strip() for x in rd.readlines()]

print(items)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


response = requests.get("https://min-api.cryptocompare.com/data/all/coinlist", headers=hdr)
theData = json.loads(response.content.decode('utf-8'))

notFound = []

for x in items:

    try:
        url = theData['Data'][x]['ImageUrl']
        filename = (x + '.png')
        dlURL = 'https://www.cryptocompare.com' + url
        print(dlURL)
        opener = urllib.request.build_opener()
        opener.addheaders = [{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(dlURL, filename)

    except Exception as e: 
        print (e)

        print("Image not found for {}".format(x))
        notFound.append(x)
