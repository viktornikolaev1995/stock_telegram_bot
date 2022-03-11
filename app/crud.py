from sqlalchemy.orm import Session
from .schemas import CategorySchema, ItemSchema
from .models import Category, Item


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, offset: int = 0, limit: int = 5):
    return db.query(Item).offset(offset).limit(limit).all()


def get_items_at_category(db: Session, category_id, offset: int = 0, limit: int = 5):
    return db.query(Item).offset(offset).limit(limit).filter(Item.category_id == category_id)

