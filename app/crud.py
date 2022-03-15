from sqlalchemy.orm import Session
from . schemas import CategoryCreateSchema, ItemCreateSchema
from . models import Category, Item


def get_stocks(db: Session, offset: int = 0, limit: int = 5):
    return db.query(Item).offset(offset).limit(limit).all()


def get_stock(db: Session, category_id, offset: int = 0, limit: int = 5):
    return db.query(Item).offset(offset).limit(limit).filter(Item.category_id == category_id)


def get_users(db: Session, offset: int = 0, limit: int = 5):
    return db.query(Category).offset(offset).limit(limit).all()


def get_user(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def create_stock(db: Session, category: CategoryCreateSchema):
    category = Category(**category.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def create_user(db: Session, item: ItemCreateSchema, ):
    item = Item(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item




