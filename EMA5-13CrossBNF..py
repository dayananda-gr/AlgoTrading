import requests,time
import pandas as pd
import pandas_ta as ta
from dhanhq import dhanhq
import datetime
import math
import csv
import urllib.parse
import yfinance as yf

dhan = dhanhq("1100892398","eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE4MzI3MTIwLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDg5MjM5OCJ9.fPgz0npiI4scf4DQcagVN9KBRZneLAw_0Rh_iQS_kPk9pINs7Wfuzd9jNlzzdf7nAhkY-YUB-iaOgUIXgfyuyQ")
Buy = False
Sell= False
start_time = datetime.time(6, 25)  # 9:15 AM
end_time = datetime.time(14, 55)  # 10:30 AM
exit_time = 180
quantity = 45
Nifty50 = ['^NSEBANK']
Existing_trade = 0


def banknifty_price_CE():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEBANK?interval=1m"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        val = price + 100
        val2 = math.fmod(val, 100)
        x = val - val2
        #print(x)
        abs_val = "{:.0f}".format(x)
        PE_PRICE = "{}".format("{:.0f}".format(x + 0))
        PE_PRICE_2 = "{}".format("{:.0f}".format(x - 100))
        print('\n Identified ATM:',"{:.0f}".format(x), 'So OTM (ATM-100) would be :',PE_PRICE_2)
        with open('bnf.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for column in csv_reader:
                    if column[9] == PE_PRICE_2 and column[10] == 'CE' :
                    #Sell Existing Position
                        print('Security ID ',column[2])
                        securityID = column[2]

        return securityID

def banknifty_price_PE():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEBANK?interval=1m"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        val = price + 100
        val2 = math.fmod(val, 100)
        x = val - val2
        #print(x)
        abs_val = "{:.0f}".format(x)
        PE_PRICE = "{}".format("{:.0f}".format(x + 0))
        PE_PRICE_2 = "{}".format("{:.0f}".format(x - 100))
        #print('\n Identified ATM:',"{:.0f}".format(x), 'So OTM (ATM-100) would be :',PE_PRICE_2)
        with open('bnf.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for column in csv_reader:
                    if column[9] == PE_PRICE_2 and column[10] == 'PE' :
                    #Sell Existing Position
                        #print('Security ID ',column[2])
                        securityID = column[2]

        return securityID

def buy_order(security_id):
   dhan.place_order(security_id=security_id,  #NiftyPE
    exchange_segment=dhan.FNO,
    transaction_type=dhan.BUY,
    quantity=quantity,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)   
    
def sell_order(security_id):
   dhan.place_order(security_id=security_id,  #NiftyPE
    exchange_segment=dhan.FNO,
    transaction_type=dhan.SELL,
    quantity=quantity,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0) 
   
def condition(stock):
    df = yf.download(stock,period='5d',interval='5m')
    print(df)
    df['EMA5'] = ta.ema(df['Close'], length=50)
    df['EMA13'] = ta.ema(df['Close'], length=21)
    df['EMA10'] = ta.ema(df['Close'], length=10)
    df['RSI']=ta.rsi(df.Close, length=16)
    #df["VWAP"]=ta.vwap(df.High, df.Low, df.Close, df.Volume)
    df = df.dropna()
    print(df)    
    return df   

while True:
    
    current_time = datetime.datetime.now().time()
    print("Current time is ",current_time)
    #time.sleep(10)
    
    # Check if current time is within the time window
    if start_time <= current_time <= end_time:
        print('Scanning started from Beginning ')
        print(dhan.get_positions())

        for stock in Nifty50:
         print(stock)
         df = condition(stock)
         if df.EMA5.iloc[-2] < df.EMA13.iloc[-2] and df.EMA5.iloc[-1] > df.EMA13.iloc[-1] and df.RSI.iloc[-1] > 50 and Buy == False :
             security_id = banknifty_price_CE()
             print(security_id)
             buy_order(security_id)
             print("CE Trade Placed successfully!")
             #print(dhan.get_positions())
             #buyprice = dhan.get_positions()
             #print(buyprice)
             #entry= buyprice['data'][6]['buyAvg']
            
             # print(dhan.get_order_by_id())
             Buy == True
             Existing_trade= security_id

         elif  df.EMA5.iloc[-2] > df.EMA13.iloc[-2] and df.EMA5.iloc[-1] < df.EMA13.iloc[-1] and df.RSI.iloc[-1] < 50 and Sell == False:        
           
             security_id = banknifty_price_PE()
             print(security_id)
             Existing_trade= security_id
             buy_order(security_id)
             Sell = True
 
             # Buy Exit criteria
         elif  df.EMA5.iloc[-2] > df.EMA13.iloc[-2] and df.EMA5.iloc[-1] < df.EMA13.iloc[-1] and Buy == True:
              security_id = Existing_trade
              sell_order(security_id)
              Buy = False
 
         elif  df.EMA5.iloc[-2] < df.EMA13.iloc[-2] and df.EMA5.iloc[-1] > df.EMA13.iloc[-1] and Sell == True:
              security_id = Existing_trade
              sell_order(security_id)
              Sell = False  
 
         elif  current_time >= end_time:        
            exit_time_start = datetime.datetime.now()
            exit_time_end = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.timedelta(seconds=exit_time)
            while datetime.datetime.now() < exit_time_end:
             print(f"Exiting trade in {round((exit_time_end - datetime.datetime.now()).total_seconds())} seconds.")
             time.sleep(1)
             # Exit the trade here
             if Buy == True:
              security_id= Existing_trade
              sell_order(security_id)              
              Buy = False
             elif Sell == True:
              security_id = Existing_trade
              sell_order(security_id)            
              Sell = False
 
            print("Trade exited successfully!")  
    else  :
        print("Waiting for Signal")    

         