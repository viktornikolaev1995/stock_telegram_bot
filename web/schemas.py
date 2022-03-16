from typing import List, Optional
from pydantic import BaseModel


class StockBase(BaseModel):
    id: int = 1

    class Config:
        orm_mode = True


class StockSchema(StockBase):
    name: Optional[str]
    symbol: str
    description: Optional[str]


class StockCreateSchema(BaseModel):
    name: Optional[str]
    symbol: str
    description: Optional[str]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int = 1
    first_name: str
    username: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserBase):
    stocks: List[int] = []


class UserSchema(UserBase):
    stocks: List[StockSchema] = []
