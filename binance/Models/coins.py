from sqlalchemy import Column,Integer,String,REAL,ForeignKey
from Models.database import Base
class SortedCoins(Base):
    __tablename__='coins'
    id=Column(Integer,primary_key=True)
    coin_name=Column(String)
    value=Column(REAL)
    def __init__(self,coin_name:str,value:REAL):
        self.coin_name=coin_name
        self.value=value
    def __repr__(self):
        info:str=f'Coin[{self.coin_name} {self.value}]'
        return info



