from typing import List

from pydantic import BaseModel


class StockBase(BaseModel):
    title: str
    description: str = ''

    class Config:
        orm_mode = True


class StockCreateSchema(StockBase):
    pass


class StockSchema(StockBase):
    id: int


class UserBase(BaseModel):
    id: int
    first_name: str
    username: str = ''

    class Config:
        orm_mode = True


class UserCreateSchema(UserBase):
    stocks: List[StockBase] = []


class UserSchema(UserBase):
    stocks: List[StockSchema] = []
