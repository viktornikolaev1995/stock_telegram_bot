from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/items/', response_model=List[schemas.ItemSchema])
def retrieve_items(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    items = crud.get_items(db, offset=offset, limit=limit)
    return items


@app.get('/items/{id}/', response_model=schemas.ItemSchema)
def retrieve_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item


@app.post('/items/', response_model=schemas.ItemSchema)
def create_item(item: schemas.ItemSchema, category_id: int = None, db: Session = Depends(get_db)):
    if category_id is not None:
        return crud.create_item(db, item=item, category_id=category_id)
    return crud.create_item(db, item=item, category_id=None)









