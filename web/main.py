import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from sqlalchemy import update


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='StockCrypto')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/stocks/', response_model=List[schemas.StockSchema], tags=['stocks'])
def retrieve_stocks(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    stocks = crud.get_stocks(db, offset=offset, limit=limit)
    return stocks


@app.get('/stocks/{symbol}/', response_model=schemas.StockSchema, tags=['stocks'])
def retrieve_stock(stock_symbol, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, stock_symbol=stock_symbol)
    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not found')

    return stock


@app.get('/users/', response_model=List[schemas.UserSchema], tags=['users'])
def retrieve_users(offset: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users


@app.get('/filter-users/', response_model=List[schemas.UserSchema], tags=['users'])
def retrieve_filter_users_at_periodic_task_field(offset: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    filter_users = crud.get_filter_users(db, offset=offset, limit=limit)
    return filter_users


@app.get('/users/{id}/', response_model=schemas.UserSchema, tags=['users'])
def retrieve_user(user_id, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.patch('/users/', response_model=schemas.UserPartialUpdate, tags=['users'])
def partial_update_user(user: schemas.UserPartialUpdateSchema, db: Session = Depends(get_db)):
    return crud.partial_update_user(db, user=user)


@app.post('/stocks/', response_model=schemas.StockSchema, tags=['stocks'])
def create_stock(stock: schemas.StockCreateSchema, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock=stock)


@app.post('/users/', response_model=schemas.UserSchema, tags=['users'])
def create_user(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    return crud.create_user(db, user=user)


@app.delete('/stocks/{id}', tags=['stocks'])
def delete_stock(stock_id: int = 1, db: Session = Depends(get_db)):
    return crud.delete_stock(db, stock_id=stock_id)


@app.delete('/users/{id}/', tags=['users'])
def delete_user(user_id: int = 1, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)




