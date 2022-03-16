import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models
from . import schemas
from . import crud
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='StockCrypto')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/stocks/', response_model=List[schemas.StockSchema])
def retrieve_stocks(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    stocks = crud.get_stocks(db, offset=offset, limit=limit)
    return stocks


@app.get('/stocks/{id}/', response_model=schemas.StockSchema)
def retrieve_stock(stock_id, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, stock_id=stock_id)

    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not found')

    return stock


@app.get('/users/', response_model=List[schemas.UserSchema])
def retrieve_users(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users


@app.get('/users/{id}/', response_model=schemas.UserSchema)
def retrieve_user(user_id, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@app.post('/stocks/', response_model=schemas.StockCreateSchema)
def create_stock(stock: schemas.StockCreateSchema, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock=stock)


@app.post('/users/', response_model=schemas.UserCreateSchema)
def create_user(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    return crud.create_user(db, user=user)



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)





