from pydantic import BaseModel


class StockCreateSchema(BaseModel):
    title: str
    description: str = ''

    class Config:
        orm_mode = True


class StockListSchema(BaseModel):
    id: int
    title: str
    description: str = ''

    class Config:
        orm_mode = True


class ItemCreateSchema(BaseModel):
    title: str
    description: str = ''
    category_id: int = 1
    archive: bool = False

    class Config:
        orm_mode = True


class ItemListSchema(BaseModel):
    id: int
    title: str
    description: str = ''
    category_id: int = None
    archive: bool = False

    class Config:
        orm_mode = True


