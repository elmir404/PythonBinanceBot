
# from typing import OrderedDict
# from binance.enums import *
# from binance.client import Client
# import config
# import math
# import time
# class Order:


    #def __init__(self):
#     def sell(self,last_price):
#         order=self.client.create_margin_order(
#             sideEffectType ="MARGIN_BUY",
#             symbol='BTCUSD',
#             side=self.client.SIDE_SELL,
#             type=self.client.ORDER_TYPE_MARKET,
#             quantity=self.max_amount_sell,
#             isIsolated="TRUE"
#         )
#         return(order)
    
#     def buy(self,last_price):
#         order=self.client.create_margin_order(
#         sideEffectType ="MARGIN_BUY",
#         symbol='BTCUSD',
#         side=self.client.SIDE_BUY,
#         type=self.client.ORDER_TYPE_MARKET,
#         quantity=((float(self.max_amount_buy)/last_price)/100*70,".5f"),
#         isIsolated="TRUE"
#         )
#         return(order)
    
#     def close_order(self,qty,side):
#         if side=="BUY":
#             order= self.client.create_margin_order(
#             symbol='BTCUSD',
#             side=self.client.SIDE_SELL,
#             type=self.client.ORDER_TYPE_MARKET,
#             quantity=qty,
#             isIsolated="TRUE",
#             sideEffectType ="AUTO_REPAY",

#             )
#         if side=="SELL":
#             order= self.client.create_margin_order(
#             symbol='BTCUSD',
#             side=self.client.SIDE_BUY,
#             type=self.client.ORDER_TYPE_MARKET,
#             quantity=qty,
#             isIsolated="TRUE",
#             sideEffectType ="AUTO_REPAY",

#             )
