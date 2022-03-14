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


@app.get('/categories/', response_model=List[schemas.CategoryListSchema])
def retrieve_categories(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, offset=offset, limit=limit)
    return categories


@app.get('/items/', response_model=List[schemas.ItemListSchema])
def retrieve_items(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    items = crud.get_items(db, offset=offset, limit=limit)
    return items


@app.get('/items/{id}/', response_model=schemas.ItemListSchema)
def retrieve_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item


@app.post('/categories/', response_model=schemas.CategoryCreateSchema)
def create_category(category: schemas.CategoryCreateSchema, db: Session = Depends(get_db)):
    return crud.create_category(db, category=category)


@app.post('/items/', response_model=schemas.ItemCreateSchema)
def create_item(item: schemas.ItemCreateSchema, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)









