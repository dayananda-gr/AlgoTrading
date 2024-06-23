import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta
import math
import csv
import requests,time
import datetime 
from dhanhq import dhanhq


dhan = dhanhq("1100892398","eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzIxMzE5NTc0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDg5MjM5OCJ9.3JP0jp0Y8YIrOZgyGccufORJs3O1q4np_PVu1M1EZArDLjDh1SnG8xTDSFTYwpbxJJ0R0bOl5EuNvWaX8vJ1JA")
Buy = False
Sell= False
start_time = datetime.time(9, 30)  # 4:45 AM
end_time = datetime.time(23, 55)  # 10:30 AM
exit_time = 180
start = (2024,5,20)
end = datetime.datetime.now()
quantity = 45
Nifty50 = ['^NSEBANK']
Trade_list = []


def PutSucurityID():
        df = yf.download('^NSEBANK',period='5d',interval='1m')
        price = df.Close.iloc[-1] 
        val = price + 100
        val2 = math.fmod(val, 100)
        x = val - val2
        #print(x)
        abs_val = "{:.0f}".format(x)
        PE_PRICE = "{}".format("{:.0f}".format(x + 0))
        PE_PRICE_2 = "{}".format("{:.0f}".format(x - 100))
        #print('\n Identified ATM:',"{:.0f}".format(x), 'So OTM (ATM-100) would be :',PE_PRICE_2)
        with open('BANKNIFTY.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for column in csv_reader:
                    if column[9] == PE_PRICE_2 and column[10] == 'PE' :
                    #Sell Existing Position
                        #print('Security ID ',column[2])
                        securityID = column[2]
        return securityID
    
       

def CallSucurityID():
        df = yf.download('^NSEBANK',period='5d',interval='1m')
        price = df.Close.iloc[-1] 
        val = price + 100
        val2 = math.fmod(val, 100)
        x = val - val2
        #print(x)
        abs_val = "{:.0f}".format(x)
        CE_PRICE = "{}".format("{:.0f}".format(x + 00))
        CE_PRICE_2 = "{}".format("{:.0f}".format(x - 100))
        print('\n Identified ATM:',"{:.0f}".format(x), 'So OTM (ATM-100) would be :',CE_PRICE_2)
        with open('BANKNIFTY.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for column in csv_reader:
                    if column[9] == CE_PRICE_2 and column[10] == 'CE' :
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
   print("Order Placed")   
    
def sell_order(security_id):
   dhan.place_order(security_id=security_id,  #NiftyPE
    exchange_segment=dhan.FNO,
    transaction_type=dhan.SELL,
    quantity=quantity,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)  


def levels(stock):
 df = yf.download(stock,period='5d',interval='5m')
 df['EMA10'] = ta.ema(df['Close'], length=10)
 df['EMA20'] = ta.ema(df['Close'], length=20)
 df['EMA5'] = ta.ema(df['Close'], length=5)
 #print(camarilladf)
 df = df.dropna()
 return df


 

while True:
    #time.sleep(10)

    current_time = datetime.datetime.now().time()
    print("Current time is ",current_time)
    
    time.sleep(3)
    
    # Check if current time is within the time window
    if start_time <= current_time <= end_time:

    
     print('Scanning started from Beginning ')
     for stock in Nifty50:
      print(stock)
      #print(dhan.get_positions())
      #security_id = CallSucurityID()
      #print(security_id)
      security_id = PutSucurityID()
      print(security_id)
      #buy_order(security_id)
      
      df = levels(stock)
      #print(df)
      
     if df.EMA5.iloc[-2] < df.EMA20.iloc[-2] and df.EMA5.iloc[-1] > df.EMA20.iloc[-1] and Buy == False :          
           
             print(" EMA 5 Crossed above EMA 20.! CE Trade Placed successfully!")
             security_id = CallSucurityID()
             print(security_id)
             buy_order(security_id)
             Existing_trade= security_id
             Buy = True 
             #print(dhan.get_positions())
             #buyprice = dhan.get_positions()
             #print(buyprice)
             #entry= buyprice['data'][6]['buyAvg']
            
             # print(dhan.get_order_by_id())

           
            #modify order  
           #dhan.modify_order(order_id, order_type, leg_name, quantity, price, trigger_price, disclosed_quantity, validity)   
     elif  df.EMA5.iloc[-2] > df.EMA20.iloc[-2] and df.EMA5.iloc[-1] < df.EMA20.iloc[-1] and Sell == False:        
           
             security_id = PutSucurityID()
             print(security_id)
             Existing_trade= security_id
             buy_order(security_id)
             Sell = True

             # Buy Exit criteria
     elif  df.EMA5.iloc[-2] > df.EMA10.iloc[-2] and df.EMA5.iloc[-1] < df.EMA10.iloc[-1] and Buy == True:
              security_id = Existing_trade
              sell_order(security_id)
              Buy = False
                # Sell Exit criteria
     elif  df.EMA5.iloc[-2] < df.EMA10.iloc[-2] and df.EMA5.iloc[-1] > df.EMA10.iloc[-1] and Sell == True:
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
        print("Waiting for EMA 5AND 20 CROSSOVER")
        
       
