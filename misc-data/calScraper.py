import pandas as pd
from bs4 import BeautifulSoup
import sys
import json
import requests

pagesWanted = 1
for i in range(1,pagesWanted+1):
    url = 'https://coinmarketcal.com/?page='+str(i)
    html_page = requests.get(url).content
    soup = BeautifulSoup(html_page, "html.parser")
    # print soup.prettify().encode("utf-8")
    articles = soup.findAll("article")
    count = 0
    for article in articles:
	count +=1
        dataList = []
        sections = article.findChildren('h5')
        print "\n"
        print "Date: " + sections[0].contents[0].contents[0].strip()
        print "Coin: " + sections[1].contents[1].contents[0].strip()
        print "Event: " + sections[2].contents[0].strip()
        desc = article.findChildren("div", {"class":"content-box-info"})
	eventID =  desc[0].get('id')
	eventID = eventID[4:]
	print "Event ID: " + eventID
        print "Date Added: " + desc[0].findChildren("p", {"class":"added-date"})[0].contents[0].encode("utf-8").strip()
        print "Details: " + desc[0].findChildren("p", {"class":"description"})[0].contents[0].encode("utf-8").strip()
        #export shit here
    print(count)
