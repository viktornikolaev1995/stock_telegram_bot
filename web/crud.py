from sqlalchemy.orm import Session
from .schemas import StockCreateSchema, UserCreateSchema
from .models import Stock, User, StockUserRelation


def get_stocks(db: Session, offset: int = 0, limit: int = 5):
    return db.query(Stock).offset(offset).limit(limit).all()


def get_stock(db: Session, stock_symbol: str):
    return db.query(Stock).filter(Stock.symbol == stock_symbol).first()


def get_users(db: Session, offset: int = 0, limit: int = 5):
    return db.query(User).offset(offset).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_stock(db: Session, stock: StockCreateSchema):
    stock = Stock(**stock.dict())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def create_user(db: Session, user: UserCreateSchema):
    db_user = User(id=user.id, first_name=user.first_name, username=user.username)
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
