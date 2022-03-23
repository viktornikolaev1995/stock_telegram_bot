from typing import List, Optional
from pydantic import BaseModel, StrictBool


class StockBase(BaseModel):
    id: int = 1
    name: Optional[str]
    symbol: str

    class Config:
        orm_mode = True
        # schema_extra = {
        #     'examples': [
        #         {
        #             'name': 'John Doe',
        #             'age': 25,
        #         }
        #     ]
        # }


class StockSchema(StockBase):
    description: Optional[str]
    country: str


class StockCreateSchema(BaseModel):
    name: Optional[str]
    symbol: str
    description: Optional[str]
    country: str

    class Config:
        orm_mode = True
        # schema_extra = {
        #     'examples': [
        #         {
        #             'name': 'John Doe',
        #             'age': 25,
        #         }
        #     ]
        # }


class UserBase(BaseModel):
    id: int = 1
    first_name: str
    username: str
    periodic_task: bool = False

    class Config:
        orm_mode = True
        # schema_extra = {
        #     'examples': [
        #         {
        #             'name': 'John Doe',
        #             'age': 25,
        #         }
        #     ]
        # }


class UserPartialUpdate(BaseModel):
    id: int = 1
    periodic_task: bool = False
    stocks: List[StockBase] = []

    class Config:
        orm_mode = True


class UserPartialUpdateSchema(BaseModel):
    id: int = 1
    periodic_task: bool = False
    stocks: List[int] = []

    class Config:
        orm_mode = True


class UserCreateSchema(UserBase):
    stocks: List[int] = []


class UserSchema(UserBase):
    stocks: List[StockBase] = []
