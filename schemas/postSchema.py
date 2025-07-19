from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str
    tags: Optional[str] = ""

class PostOut(PostCreate):
    id: int
    author_id: int

    class Config:
        orm_mode = True
