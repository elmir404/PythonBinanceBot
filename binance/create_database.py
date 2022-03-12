from Models.base import BaseCoin
from sqlalchemy.orm import session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.sqltypes import Float, Numeric
from Models import buycoins, coins
from Models.database import create_db, Session
from Models.coins import SortedCoins
from Models.buycoins import BuyCoins
from collections import defaultdict

def create_database(load_fake_data: bool = True):
    create_db()
    if load_fake_data:
        _load_fake_data()
        load_buyed_coins()


def _load_fake_data(session: Session,coini):
       session=Session()
       for key,value in coini.items():
        coins=SortedCoins(coin_name=key,value=value)
        session.add(coins)
       session.commit()
       session.close()

def load_buyed_coins(session: Session,buyedCoins):
       session=Session()
       for key,value in buyedCoins.items():
        buycoins=BuyCoins(coin_name=key,buyPrice=value[0],quantity=value[1])
        session.add(buycoins)
       session.commit()
       session.close()
   
def get_data():
    session=Session()
   # c=session.query(SortedCoins.coin_name,SortedCoins.value).order_by(SortedCoins.id.desc()).limit(30)
    c=session.query(SortedCoins.coin_name,SortedCoins.value).order_by(SortedCoins.id.desc()).limit(200)
    c=c[::-1]
    # ten={}
    # for key,value in c:
    #     print(key)
    #     ten[key]=value
    
    return c
def get_buyed_coins():
    session=Session()
   # c=session.query(SortedCoins.coin_name,SortedCoins.value).order_by(SortedCoins.id.desc()).limit(30)
    s=session.query(BuyCoins.coin_name,BuyCoins.buyPrice,BuyCoins.quantity).all()
    if s==[]:
        return 0
    return s
def get_base_coins():
    session=Session()
   # c=session.query(SortedCoins.coin_name,SortedCoins.value).order_by(SortedCoins.id.desc()).limit(30)
    s=session.query(BaseCoin.coin_name).all()
    if s==[]:
        return 0
    return s
def delete_coin(coinName:str):
    session=Session()
    a=session.query(BuyCoins).filter(BuyCoins.coin_name==coinName).first()
    session.delete(a)
    session.commit()
def clear_table():
    session=Session()
    a=session.query(SortedCoins).delete()
    session.commit()
    

    