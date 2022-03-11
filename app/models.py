from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default='')

    items = relationship('Item', back_populates='category')


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default='')
    category_id = Column(Integer, ForeignKey('categories.id'))
    archive = Column(Boolean, default=False)

    category = relationship('Category', back_populates='items')