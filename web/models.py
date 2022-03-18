from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


class StockUserRelation(Base):
    __tablename__ = 'stockuserrelation'

    stock_id = Column(ForeignKey('stock.id'), primary_key=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True)

    stock = relationship('Stock', back_populates='users')
    user = relationship('User', back_populates='stocks')


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='')
    symbol = Column(String, unique=True)
    description = Column(String, default='')
    users = relationship(StockUserRelation, back_populates='stock')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    username = Column(String, index=True)
    stocks = relationship(StockUserRelation, back_populates='user')
