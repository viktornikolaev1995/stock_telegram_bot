from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class StockUserRelation(Base):
    __tablename__ = 'stockuserrelation'

    stock_id = Column(ForeignKey('stock_table.id'), primary_key=True)
    user_id = Column(ForeignKey('user_table.id'), primary_key=True)
    # stock = relationship('Stock', back_populates='users')
    # user = relationship('User', back_populates='stocks')


class Stock(Base):
    __tablename__ = 'stock_table'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, default='')
    symbol = Column(String, unique=True, index=True)
    description = Column(String, default='')
    country = Column(String)
    # users = relationship('StockUserRelation')


class User(Base):
    __tablename__ = 'user_table'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    first_name = Column(String)
    username = Column(String, unique=True, index=True)
    periodic_task = Column(Boolean, default=False)
    stocks = relationship('Stock', secondary='stockuserrelation')


# class Show(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), unique=True, nullable=False)
#     studio = db.relationship("Studio", secondary="show_studio",
#                              back_populates="show")
#
# class Studio(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     show = db.relationship("Show", secondary="show_studio",
#                            back_populates="studio")
#
# class ShowStudio(db.Model):
#     show_id = db.Column(db.Integer, db.ForeignKey(Show.id, ondelete="CASCADE"),
#                         primary_key=True)
#     studio_id = db.Column(db.Integer, db.ForeignKey(Studio.id, ondelete="CASCADE"),
#                           primary_key=True)
