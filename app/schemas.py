from pydantic import BaseModel


class CategorySchema(BaseModel):
    title: str
    description: str = ''


class ItemSchema(BaseModel):
    title: str
    description: str = ''
    category: int = 1
    archive: bool = False
