from sqlalchemy import Column,Integer,String,REAL,ForeignKey
from Models.database import Base
class BuyCoins(Base):
    __tablename__='buycoins'
    id=Column(Integer,primary_key=True)
    coin_name=Column(String)
    quantity=Column(REAL)
    buyPrice=Column(REAL)
    def __init__(self,coin_name:str,buyPrice:REAL,quantity:REAL):
        self.coin_name=coin_name
        self.buyPrice=buyPrice
        self.quantity=quantity
    def __repr__(self):
        info:str=f'Coin[{self.coin_name}{self.buyPrice}{self.quantity}]'
        return info
