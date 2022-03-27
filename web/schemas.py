from typing import List, Optional
from pydantic import BaseModel, StrictBool


class StockBase(BaseModel):
    id: int = 1
    name: Optional[str]
    symbol: str

    class Config:
        orm_mode = True


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
        schema_extra = {
            'example':
                {
                    'name': 'PayPal Holdings Inc',
                    'symbol': 'PYPL',
                    'description': '',
                    'country': 'united states'
                }
        }


class UserBase(BaseModel):
    id: int = 1
    first_name: str
    username: str
    periodic_task: bool = False

    class Config:
        orm_mode = True
        schema_extra = {
            'example':
                {
                    'id': 1,
                    'first_name': 'Mikel',
                    'username': 'mikel',
                    'periodic_task': False
                }
            }


class UserProfilePartialUpdateSchema(BaseModel):
    id: int = 1
    first_name: str
    username: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example':
                {
                    'id': 1,
                    'first_name': 'Mikel',
                    'username': 'mikel',
                }
            }


class UserPeriodicTaskPartialUpdateSchema(BaseModel):
    id: int = 1
    periodic_task: bool = False

    class Config:
        orm_mode = True
        schema_extra = {
            'example':
                {
                    'id': 1,
                    'periodic_task': False,
                }
            }


class UserStocksPartialUpdateSchema(BaseModel):
    id: int = 1
    stocks: List[int] = []

    class Config:
        orm_mode = True
        schema_extra = {
            'example':
                {
                    'id': 1,
                    'stocks': [1, 2]
                }
            }


class UserCreateSchema(UserBase):
    stocks: List[int] = []

    class Config:
        orm_mode = True
        schema_extra = {
            'example':
                {
                    'id': 1,
                    'first_name': 'Mikel',
                    'username': 'mikel',
                    'periodic_task': False,
                    'stocks': [1, 2]
                }
        }


class UserSchema(UserBase):
    stocks: List[StockBase] = []

    class Config:
        orm_mode = True
