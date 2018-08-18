from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
import sys
import json
import getpass
 
try:
    print("Welcome to the crypto techical data library!")
    password = getpass.getpass("Enter the password:")
    if (password == "supreme2018"):
        print("Authenticated! Welcome :)")
 
    else:
        print("Invalid Password! Exiting...")
        sys.exit()
 
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-gpu')
    options.add_argument('--silent')
    options.add_argument("--log-level=3")  # fatal
 
    while True:
        data={"symbols":{"tickers":["BITFINEX:BTCUSD"],"query":{"types":[]}},"columns":["Recommend.Other","Recommend.All","Recommend.MA","RSI","RSI[1]","Stoch.K","Stoch.D","Stoch.K[1]","Stoch.D[1]","CCI20","CCI20[1]","ADX","ADX+DI","ADX-DI","ADX+DI[1]","ADX-DI[1]","AO","AO[1]","Mom","Mom[1]","MACD.macd","MACD.signal","Rec.Stoch.RSI","Stoch.RSI.K","Rec.WR","W.R","Rec.BBPower","BBPower","Rec.UO","UO","EMA10","close","SMA10","EMA20","SMA20","EMA30","SMA30","EMA50","SMA50","EMA100","SMA100","EMA200","SMA200","Rec.Ichimoku","Ichimoku.BLine","Rec.VWMA","VWMA","Rec.HullMA9","HullMA9","Pivot.M.Classic.S3","Pivot.M.Classic.S2","Pivot.M.Classic.S1","Pivot.M.Classic.Middle","Pivot.M.Classic.R1","Pivot.M.Classic.R2","Pivot.M.Classic.R3","Pivot.M.Fibonacci.S3","Pivot.M.Fibonacci.S2","Pivot.M.Fibonacci.S1","Pivot.M.Fibonacci.Middle","Pivot.M.Fibonacci.R1","Pivot.M.Fibonacci.R2","Pivot.M.Fibonacci.R3","Pivot.M.Camarilla.S3","Pivot.M.Camarilla.S2","Pivot.M.Camarilla.S1","Pivot.M.Camarilla.Middle","Pivot.M.Camarilla.R1","Pivot.M.Camarilla.R2","Pivot.M.Camarilla.R3","Pivot.M.Woodie.S3","Pivot.M.Woodie.S2","Pivot.M.Woodie.S1","Pivot.M.Woodie.Middle","Pivot.M.Woodie.R1","Pivot.M.Woodie.R2","Pivot.M.Woodie.R3","Pivot.M.Demark.S1","Pivot.M.Demark.Middle","Pivot.M.Demark.R1"]}
        ticker = raw_input("Enter a valid ticker (Ex: BTCUSD): ").upper()
        url="https://www.tradingview.com/symbols/"+ticker+"/technicals/"
        timeframe = raw_input("Enter a timeframe (Options are: '15m', '1hr', '1d', '1w', '1m'): ")
        if timeframe.lower() not in ('15m','1hr','1d','1w','1m'):
            print("Invalid time frame! Options are: '15m', '1hr', '1d', '1w', '1m'")
            continue
        else:
            if timeframe.lower() == '15m':
                timeframe = '15 minutes'
                data["columns"] = [thing.replace('|', '|15') for thing in data["columns"]]
            elif timeframe.lower() == '1hr':
                timeframe = '1 hour'
                data["columns"] = [thing.replace('|', '|60') for thing in data["columns"]]
            elif timeframe.lower() == '1d':
                timeframe = '1 day'
            elif timeframe.lower() == '1w':
                timeframe = '1 week'
                data["columns"] = [thing.replace('|', '|1W') for thing in data["columns"]]
            elif timeframe.lower() == '1m':
                timeframe = '1 month'
                data["columns"] = [thing.replace('|', '|1M') for thing in data["columns"]]
        html_page = None
        timeframeString = "//div[contains(text(),'"+timeframe+"')]"
        try:
            # Start the WebDriver and load the page
            wd = Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)
            wd.get(url)
            element = wd.find_element_by_xpath(timeframeString)
            element.click()
            response = wd.request('POST', 'https://scanner.tradingview.com/crypto/scan', data=json.dumps(data))
            # Wait for the dynamically loaded elements to show up
            WebDriverWait(wd, 1)
            # And grab the page HTML source
            html_page = wd.page_source
            wd.quit()
        except Exception as e:
            print e
            print ("Invalid Ticker! Example: BTCUSD")
            continue
 
        # Now you can use html_page as you like
        soup = BeautifulSoup(html_page, "html.parser")
        tables = soup.findAll("table")
 
        df1_cols = ['Indicator', 'Value', 'Rating']
        df2_cols = ['Name', 'S3', 'S2', 'S1', 'P', 'R1', 'R2', 'R3']
 
        for table in tables:
            dataList = []
            tableName = table.findChildren('a')[0].contents
            if table.findParent("table") is None:
                rows = table.findChildren('tr')
                for row in rows:
                    data = []
                    cells = row.findChildren('td')
                    for cell in cells:
                        value = cell.string
                        #print "The value in this cell is " + value.encode('ascii','ignore')
                        if len(cells) == 3 or len(cells) == 8:
                            data.append(value.encode('ascii','ignore'))
                    if len(data) != 0:
                        dataList.append(data)
                if tableName[0] == u'Oscillators':
                    dfOscillators = pd.DataFrame(dataList,columns=df1_cols)
                elif tableName[0] == u'Moving Averages':
                    dfIndicators = pd.DataFrame(dataList,columns=df1_cols)
                elif tableName[0] == u'Pivots':
                    dfPivots = pd.DataFrame(dataList,columns=df2_cols)
 
        pd.set_option('colheader_justify', 'right')
        print ("\nTechnical Data for Ticker: " + ticker + " with time frame: " + timeframe)
        print ("Oscillators")
        print tabulate(dfOscillators, headers='keys', tablefmt='psql',showindex='never')
        print ("Moving Averages")
        print tabulate(dfIndicators, headers='keys', tablefmt='psql',showindex='never')
        print ("Pivots")
        print tabulate(dfPivots, headers='keys', tablefmt='psql',showindex='never')
        print ("\n")
except KeyboardInterrupt:
    None
except Exception as e:
    print e
    None
