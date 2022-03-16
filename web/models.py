from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


StockUserRelation = Table(
    'association', Base.metadata,
    Column('stock', ForeignKey('stock.id'), primary_key=True),
    Column('user', ForeignKey('user.id'), primary_key=True)
)


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='')
    symbol = Column(String, unique=True)
    description = Column(String, default='')
    users = relationship(
        'User',
        secondary=StockUserRelation,
        backref='users'
    )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    username = Column(String, index=True)
    stocks = relationship(
        Stock,
        secondary=StockUserRelation,
        backref='stocks'
    )


