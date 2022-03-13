from pydantic import BaseModel


class CategorySchema(BaseModel):
    title: str
    description: str = ''


class ItemSchema(BaseModel):
    title: str
    description: str = ''
    # category_id: int = None
    archive: bool = False
