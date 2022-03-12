from operator import le
from sqlalchemy.sql.expression import false
import config
from sqlalchemy import and_
#from order import Order
from Models.database import DATABASE_NAME,Session
import create_database as db_creator
from Models.coins import SortedCoins
import os
from binance.client import Client
from binance.exceptions import *
from decimal import Decimal as D, ROUND_DOWN, ROUND_UP
from collections import defaultdict
from binance.exceptions import BinanceAPIException
import time
import pandas as pd
import numpy as np
import math
class Main:
    def __init__(self):
        self.client =Client(api_key=config.api_key,api_secret=config.api_secret,tld='com')
        #self.client.API_URL=config.url
        print("Giriş edildi!")
        print("--------------------------------------------------------------------")
        # a=self.account_info()
        # b=self.top_ten()
        # d=self.buy_coins()
        # self.sat()
        self.start_trade()
        #db.create_database()
        #db.set_coins(b)
        #super().__init__("sqlite:///")
    def start_trade(self):
        while True:
                print("Hesab balansi gətirilir....")
                time.sleep(1)
                balance =self.client.get_asset_balance('USDT')
                quan=self.client.get_account()
                print(quan)
                if balance ==None:
                    print("Hesabınızda məbləğ yoxdur")
                    break
                else:
                    print(f"hesab balansi:{balance['free']} USDT")
                    orrder_bal=float(balance['free'])/10
                    order_b1=round(orrder_bal,7)
                    print(f"Hər coin üçün ayrılan miqdar{order_b1}")
                #accon=self.client.get_account()
                #print(accon)
                


               #ortalamasi en yuksek top 10 coin
                
                print("Seçilmiş coinlər məlumat bazasına əlavə edilir.....")

                # klines = self.client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
                # print("Klineler:",klines)
                coins={}
                sorted_coins={}
                # base_coins=db_creator.get_base_coins()
                # for t in base_coins:
                try:


                    coin=self.client.get_ticker()
                    for coins1 in coin:
                        s=coins1['symbol']
                        chck=s[-4:]
                    # print(f"{s}-in ticarət üçün uyğunluğu yoxlanılır!")
                        trading_info=self.client.get_symbol_info(symbol=s)
                    # klines = self.client.get_klines(symbol=t[0], interval='5m', limit='500')
                    # close = [float(entry[4]) for entry in klines]
                    # close_array = np.asarray(close)
                    # close_finished = close_array[:-1]
                    # rsi = self.computeRSI(data=close_finished, time_window=14)
                        last=float(coins1['lastPrice'])
                        avg=float(coins1['weightedAvgPrice'])
                    # lowP=float(coin['lowPrice'])

                        if chck=="USDT" and s !="BNBUSDT" and trading_info['status']=="TRADING" and s.find("UP")==-1 and s.find("DOWN")==-1:
                            c=last/avg
                            coins[s]=c
                            print(f"{s}-in ticarət üçün uyğundur!Məlumat bazasına əlavə edildi")
                        else:
                            time.sleep(1)
                            print(f"{s}-in ticarət üçün uyğun deyil!")
                except Exception as e:
                        print("Coinler getirilerkien xeta bash verdi!",e)

                sorted_coins=dict(sorted(coins.items(),key=lambda x:x[1],reverse=True))
                db_creator._load_fake_data(session=Session(),coini=sorted_coins)
                print("Əməliyyat tamamlandı!!!!!!!")
                print("Ortalamsı ən az 200 coin bazadan gətirilir....")
                ten=db_creator.get_data()
                say=0
                time.sleep(3)
                print('Coin alışında istifadə edəcəyiniz məbləğ:',order_b1)
                dic = defaultdict(list)
                say1=10
                if order_b1>20:
                    for key,value in ten:
                        time.sleep(2)
                        try:
                            balance1 =self.client.get_asset_balance('USDT')
                            if say1!=0:
                                order_b1=float(balance1['free'])/say1
                            print("coin alisinda istifade olunan mebleqqqqqq:",order_b1)
                            minp=self.client.get_symbol_info(symbol=key)
                            stepSize1=minp['filters'][2]['stepSize']
                            if stepSize1.find("1")==0:
                                1-stepSize1.find(".")
                            step=stepSize1.find("1")-1
                            minQty=float(minp['filters'][2]['minQty'])
                            print("Minimum miqdar:",minQty)
                            maxQty =float(minp['filters'][2]['maxQty'])
                            btc_price = self.client.get_symbol_ticker(symbol=key)
                            quantity1=(math.floor(order_b1*10**float(step)/float(btc_price['price']))/float(10**step))
                            step=round(float(quantity1-minQty) % float(stepSize1),2)   
                            print(f"{key} son qiymeti:{btc_price['price']},Alış üçün miqdar {quantity1}.")
                        except Exception as e:
                            print("Baglanti xetasi:",e)
                        if 1==1 :#quantity1>minQty and quantity1<maxQty and step==0.0:
                            if order_b1<10:
                                 break  
                            try:
                                order = self.client.create_order(
                                        symbol=key,
                                        side=self.client.SIDE_BUY,
                                        type=self.client.ORDER_TYPE_LIMIT,
                                        timeInForce=self.client.TIME_IN_FORCE_GTC,
                                        quantity=quantity1,
                                        price=float(btc_price['price'])
                                   )
                            except Exception as e:
                                print("Alish zamani sehv bashv verdi!:",e)
                                continue
                            time.sleep(1)
                            order1=self.client.get_order(symbol=key,orderId=order['orderId'],) 
                            if order1['status']=='NEW':
                                print("Alışın tamamlanması üçün gözlənilir....")
                            order1=self.client.get_order(symbol=key,orderId=order['orderId'],)
                            if order1['status']=='NEW' :
                                try:
                                    result = self.client.cancel_order(
                                                symbol=key,
                                                orderId=order['orderId'])
                                except Exception as e:
                                    print("Emeliyat silinen zaman sehv yarandi")
                                    order1=self.client.get_order(symbol=key,orderId=order['orderId'],)
                                    print("Alish statusu:",order1['status'])
                                    if order1['status'] =="FILLED" or order1['status'] =="PARTIALLY_FILLED":
                                        print(f"{key} i aldınız!")
                                        a=[]
                                        print(order1)
                                        say=say+1
                                        say1=say1-1
                                        a.append(btc_price['price'])
                                        a.append(quantity1)
                                        dic[key]=a
                                        buyed_coins=dict(sorted(dic.items(),key=lambda x:x[1],reverse=True))
                                        db_creator.load_buyed_coins(session=Session(),buyedCoins=buyed_coins)
                                        print(dic)
                                        dic = defaultdict(list)
                                        continue
                            order1=self.client.get_order(symbol=key,orderId=order['orderId'],) 
                            order1=self.client.get_order(symbol=key,orderId=order['orderId'],)
                            print("Alish statusu:",order1['status'])
                            if order1['status'] =="FILLED" or order1['status'] =="PARTIALLY_FILLED":
                                print(f"{key} i aldınız!")
                                a=[]
                                print(order1)
                                say=say+1
                                say1=say1-1
                                a.append(btc_price['price'])
                                a.append(quantity1)
                                dic[key]=a
                                buyed_coins=dict(sorted(dic.items(),key=lambda x:x[1],reverse=True))
                                db_creator.load_buyed_coins(session=Session(),buyedCoins=buyed_coins)
                                print(dic)
                                dic = defaultdict(list)
                           
                            print("Say:",say)
                        if say==10:
                            break    
                # db_creator.clear_table()
                while True:
                    coins=db_creator.get_buyed_coins()
                    if coins==0:
                        break
                    for coin in coins:
                        try:
                            
                            minp=self.client.get_symbol_info(symbol=coin[0])
                            stepSize1=minp['filters'][2]['stepSize']
                            maxQty=float(minp['filters'][2]['maxQty'])
                            minQty=float(minp['filters'][2]['minQty'])
                            print("Maksimim alish miqdari:",maxQty)
                            print("Minimum alish miqdari:",minQty)
                            if stepSize1.find("1")==0:
                                1-stepSize1.find(".")
                            step=stepSize1.find("1")-1
                            symbol=coin[0].replace("USDT","")
                            time.sleep(1)
                            quantity =self.client.get_asset_balance(symbol)
                            print(f"{symbol} hesab coin balansiniz:",quantity['free'])
                            quantity =float(quantity['free'])
                            print(quantity)
                            quantity =math.floor(float(quantity)*10**step)/float(10**step)    
                            print(quantity)
                            btc_price = self.client.get_symbol_ticker(symbol=coin[0])
                        except Exception as e:
                            print("Coin melumatlari getirilerken xeta bash verdi!")
                            continue
                        if quantity==0.0 or quantity< minQty:
                            print("Satış üçün tələb olun coin hesabınızda mövcud deyil!")
                            db_creator.delete_coin(coinName=coin[0])
                        else:      
                            if quantity!=0.0:
                                if float(btc_price['price'])>= float(coin[1])*1.02 or float(btc_price['price'])<= float(coin[1])*0.85:
                                    try:
                                        order = self.client.create_order(
                                            symbol=coin[0],
                                            side=self.client.SIDE_SELL,
                                            type=self.client.ORDER_TYPE_LIMIT,
                                            timeInForce=self.client.TIME_IN_FORCE_GTC,
                                            quantity=quantity,
                                            price=float(btc_price['price'])
                                        )
                                    except Exception as e:
                                        print("Satish zamani xeta yarandi.")
                                        break
                                       
                                    time.sleep(1)
                                    order1=self.client.get_order(symbol=coin[0],orderId=order['orderId'],)
                                    print(order1)
                                    if order1['status']=="NEW":
                                      print("Satışın tamamlanması üçün gözlənilir....")
                                      time.sleep(1)
                                    print("Satish statusu:",order1['status'])
                                    order1=self.client.get_order(symbol=coin[0],orderId=order['orderId'],)
                                    if order1['status']=="PARTIALLY_FILLED" or order1['status']=="NEW":
                                        try:
                                            result = self.client.cancel_order(
                                                        symbol=coin[0],
                                                        orderId=order['orderId'])
                                        except Exception as e:
                                            print("Emeliyyat silinerken sehv yarandi")
                                        
                                    order1=self.client.get_order(symbol=coin[0],orderId=order['orderId'],)
                                    print("Satish statusu:",order1['status'])
                                    if order1['status']=="FILLED":                               
                                        print(f"{coin[0]} satildi!")
                                else:
                                    
                                    print(f"{coin[0]} -in qiymət artımı satış üçün uyğun deyil.Digər coin yoxlanılır!")

    def computeRSI(self, data, time_window):
        diff = np.diff(data)
        up_chg = 0 * diff
        down_chg = 0 * diff

        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[diff > 0]

        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[diff < 0]

        up_chg = pd.DataFrame(up_chg)
        down_chg = pd.DataFrame(down_chg)

        up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
        down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

        rs = abs(up_chg_avg / down_chg_avg)
        rsi = 100 - 100 / (1 + rs)
        rsi = int(rsi[0].iloc[-1])
        return rsi














    # def start_trade(self):
#     self.trading =Order()
#     print("Starting new trade")
#     while True:

#         try:
#             klines=self.client.get_historical_klines("BTCUSDT",self.client.KLINE_INTERVAL_15MINUTE,"1 day ago utc")
#         except:
#             print('Timeout!Waiting for time binace to respond...')
#             time.sleep(120)
#             print('Trying to connect again')
#             klines=self.client.get_historical_klines("BTCUSDT",self.client.KLINE_INTERVAL_15MINUTE,"1 day ago utc")
        
#         prices=[]
#         for i in klines:
#             prices.append(float(i[4]))
        
#         last_RSI=talib.RSI(numpy.asarray(prices),14)[-1]
#         if last_RSI >55:
#             self.order_to_track=self.trading.buy(prices[len(prices)-1])
#             self.track_trade()
#         elif last_RSI<45:
#             self.order_to_track=self.trading.buy(prices[len(prices)-1])
#             self.track_trade()
#         else:
#             time.sleep(1.5)
#             print('RSI :',last_RSI)
#             print('No enter points,loking again...')




# def track_trade(self):
#     def precent_change(original,new):
#         original =float(original)
#         new =float(new)
#         return (original -new )/original*100
#     while True:
#         time.sleep(1.5)
#         try:
#             self.last_price=self.client.get_recent_trades(symbol='BTCUSDT')[-1]['price']
#         except:1
#             print('Timeout!Waiting for binance to respond...')
#             time.sleep(120)
#             print('Typing to connect again...')
#         change=precent_change(self.order_to_track['fills'][0]['price'],self.last_price)
#         if(self.order_to_track['side']=="SELL"):
#             change  =change*-1
#         if change >=0.5 or change <=-0.6:
#             print(change)
#             self.end_trade()
#             print('current trade ended with profit of:',change,'%')
#             time.sleep(1.5)
#             try:
#                 self.start_trade()
    #             except:
    #                 print("can't make new trade,trying again  in 30 sec...")
    #                 time.sleep(30)
    #                 self.start_trade( )

    #         else:
    # def end_trade(self):
    #     self.trading.close_order(self.order_to_track['executeQty'],self.order_to_track['side'])
    #              print('current trade profit:',format(change,'2f'),"%")
    #    print('end.Order finished successfully')


    #session = Session()
    #session.add(Coin(coin_name="231323",value=2132321))
    #session.commit()
#Main()
if __name__ == "__main__":
    db_is_created=os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_database()
    session=Session()
Main()
