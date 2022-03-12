from sqlalchemy import Column,Integer,String,REAL,ForeignKey
from Models.database import Base
class BaseCoin(Base):
    __tablename__='basecoins'
    id=Column(Integer,primary_key=True)
    coin_name=Column(String)
    def __init__(self,coin_name:str):
        self.coin_name=coin_name
    def __repr__(self):
        info:str=f'Coin[{self.coin_name}]'
        return info