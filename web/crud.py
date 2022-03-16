from sqlalchemy.orm import Session
from .schemas import StockCreateSchema, UserCreateSchema, StockSchema, UserSchema
from .models import Stock, User


def get_stocks(db: Session, offset: int = 0, limit: int = 5):
    return db.query(StockSchema).offset(offset).limit(limit).all()


def get_stock(db: Session, stock_id, offset: int = 0, limit: int = 5):
    return db.query(StockSchema).offset(offset).limit(limit).filter(Stock.id == stock_id)


def get_users(db: Session, offset: int = 0, limit: int = 5):
    return db.query(UserSchema).offset(offset).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(UserSchema).filter(UserSchema.id == user_id).first()


def create_stock(db: Session, stock: StockCreateSchema):
    stock = Stock(**stock.dict())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def create_user(db: Session, user: UserCreateSchema):
    user = User(id=user.id, first_name=user.first_name, username=user.username)
    stocks = db.query(Stock).filter(Stock.id in user.stocks)
    for stock in stocks:
        user.stocks.append(stock)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user



# def create_user_groups(db: Session, user_groups: schemas.UserGroupsBase):
#     db_user = db.query(models.User).filter(models.User.id == user_groups.id_user).first()
#     db_group = db.query(models.Group).filter(models.Group.id == user_groups.id_group).first()
#
#     if not db_user and db_group:
#         raise HTTPException(status_code=409, detail="User or Group not found in system.")
#
#     db_user.groups.append(db_group)
#
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user




