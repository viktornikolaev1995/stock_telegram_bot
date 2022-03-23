from typing import Optional

from sqlalchemy.orm import Session
from .schemas import StockCreateSchema, UserCreateSchema, UserSchema, UserPartialUpdateSchema
from .models import Stock, User, StockUserRelation


def get_stocks(db: Session, offset: int = 0, limit: int = 5):
    return db.query(Stock).offset(offset).limit(limit).all()


def get_stock(db: Session, stock_symbol: str):
    return db.query(Stock).filter(Stock.symbol == stock_symbol).first()


def get_users(db: Session, offset: Optional[int] = None, limit: Optional[int] = None):
    if offset is None and limit is not None:
        return db.query(User).limit(limit).all()

    elif offset is not None and limit is None:
        return db.query(User).offset(offset).all()

    elif offset is not None and limit is not None:
        return db.query(User).offset(offset).limit(limit).all()

    else:
        return db.query(User).all()


def get_filter_users(db: Session, offset: Optional[int] = None, limit: Optional[int] = None):
    if offset is None and limit is not None:
        return db.query(User).filter_by(periodic_task=True).limit(limit).all()

    elif offset is not None and limit is None:
        return db.query(User).filter_by(periodic_task=True).offset(offset).all()

    elif offset is not None and limit is not None:
        return db.query(User).filter_by(periodic_task=True).offset(offset).limit(limit).all()

    else:
        return db.query(User).filter_by(periodic_task=True).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def partial_update_user(db: Session, user: UserPartialUpdateSchema):
    # db_user = User(id=user.id, first_name=user.first_name, username=user.username, periodic_task=user.periodic_task)
    # db_stocks = db.query(Stock).filter(Stock.id.in_((user.stocks))).all()
    #
    # # for stock in db_stocks:
    # #     db_user.stocks.append(stock)
    # payload = {
    #     'id': db_user.id,
    #     'first_name': db_user.first_name,
    #     'username': db_user.username,
    #     'periodic_task': db_user.periodic_task,
    # }
    db_user = db.query(User).filter(User.id == user.id).first()
    db_user.periodic_task = user.periodic_task
    db_user.stocks = []
    db_stocks = db.query(Stock).filter(Stock.id.in_((user.stocks))).all()

    for stock in db_stocks:
        db_user.stocks.append(stock)

    db.commit()

    return user
    # return db.query(User).filter(User.id == user.id).update()


def create_stock(db: Session, stock: StockCreateSchema):
    stock = Stock(**stock.dict())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def create_user(db: Session, user: UserCreateSchema):
    db_user = User(id=user.id, first_name=user.first_name, username=user.username, periodic_task=user.periodic_task)
    db_stocks = db.query(Stock).filter(Stock.id.in_((user.stocks))).all()

    for stock in db_stocks:
        db_user.stocks.append(stock)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_stock(db: Session, stock_id):
    db.query(Stock).filter(Stock.id == stock_id).delete()
    db.commit()
    return {'204': 'Successful Response'}


def delete_user(db: Session, user_id):
    db.query(StockUserRelation).filter(StockUserRelation.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {'204': 'Successful Response'}
